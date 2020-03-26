import asyncio
import httpx
import aiofiles
import os
from functools import wraps
from opnieuw import retry_async, retry
from urllib.parse import urlparse

class WebHdfsAsyncClient():
    def __init__(self, url, user, kilobyte_chunks=64, retry_attempts=4, retry_seconds=60, kerberos_token=None):
        self._url = url
        self._user = user        
        self._kilobyte_chunks = int(kilobyte_chunks)
        self._retry_attempts = retry_attempts
        self._retry_seconds = retry_seconds
        self._kerberos_token = kerberos_token

    def _kerberize(f):
        @wraps(f)
        def wrapper(token, *args, **kwargs):
            kwargs['kerberos_token'] = token
            f(*args, **kwargs)
        return wrapper

    async def _file_sender(self, file_name=None):
        async with aiofiles.open(file_name, 'rb') as f:
            chunk = await f.read(self._kb_chunks*1024)
            while chunk:
                yield chunk
                chunk = await f.read(self._kb_chunks*1024)

    async def create(self, destination : str, origin : str, **kwargs):
        @retry_async(
            retry_on_exceptions=(httpx.HTTPError, httpx.ConnectionClosed),
            max_calls_total=self._retry_attempts,
            retry_window_after_first_call_in_seconds=self._retry_seconds,
        )
        async def _create(self, destination : str, origin : str, **kwargs):
            async with httpx.AsyncClient() as session:
                params = {
                    'op' : 'CREATE',
                    'overwrite' : str(kwargs.get('overwrite', False)).lower(),
                    'user.name' : self._user
                }

                # Kerberos verification
                if self._token:
                    params = {**params, **{'delegation' : self._token}}

                response_name_node = await session.put(f'{self._url}/webhdfs/v1{destination}', params=params, allow_redirects=False)
                response_data_node = await session.put(
                            response_name_node.headers['location'],
                            data=self._file_sender(file_name=origin),
                            params={'delegation' : self._token},
                            timeout=30*60 # 30 minutes
                )

                total_size = os.path.getsize(origin)
                succ = response_data_node.status_code == 201
                body = response_data_node.text
                hdfs_path = urlparse(response_data_node.headers['location']).path
                return HDFSOp(hdfs_path, 'CREATE', total_size, succ)
        return _create(self, destination, origin, **kwargs)