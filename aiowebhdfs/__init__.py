import asyncio
import httpx
import aiofiles
from opnieuw import retry_async
from furl import furl


class WebHdfsAsyncClient():
    _retry_attempts = 3
    _retry_seconds = 10

    def __init__(
            self, host, port, user, transport='https', endpoint='webhdfs', api_version='v1', kilobyte_chunks=512,
            retry_attempts=3, retry_seconds=60, timeout_seconds=60, kerberos_token=None):
        '''
        A modern asynchronous library to operate on WebHdfs.

        Args:
            host (str): The server name typically the NameNode of your Hadoop implementation
            port (int): Port number for WebHDFS configuration
            transport (str): http or https. Default to https
            endpoint (str): WebHDFS API endpoint. Default to webhdfs
            api_version (str): Current version as per Hadoop 3.2.1. Default to v1
            kilobyte_chunks (int): Amount of kilobytes used to stream files when uploading. Default to 512
            timeout_seconds (int): Time after a web request will timeout. Default 60 seconds
            kerberos_token (str): If set, will pass the delegation parameter in the URI. Defaults to None
            @class retry_attemps (int): Currently fixed at 3. Implemented through opnieuw library
            @class retry_seconds (int): Currently fixed at 1o seconds. Implemented through opnieuw library
        '''
        self._host = host
        self._port = port
        self._user = user
        self._transport = transport
        self._endpoint = endpoint
        self._api_version = api_version
        self._kilobyte_chunks = int(kilobyte_chunks)
        self._kerberos_token = kerberos_token
        self._timeout_seconds = timeout_seconds
        self._url = furl(f'{transport}://{host}:{port}')
        self._url /= endpoint
        self._url /= api_version

        # Class Defaults
        _retry_attempts = retry_attempts
        _retry_seconds = retry_seconds

    def __repr__(self):
        '''Information about this WebHdfsAsyncClient'''
        return f'Host: {self._host}\nPort: {self._port}\nUser: {self._user}\n End: {self._endpoint}\n Api: {self._api_version}\n URL: {self._url}'

    async def _file_sender(self, file_name=None):
        'Helper method to stream data files into HDFS in chunks of kilobytes'
        async with aiofiles.open(file_name, 'rb') as f:
            chunk = await f.read(self._kilobyte_chunks*1024)
            while chunk:
                yield chunk
                chunk = await f.read(self._kilobyte_chunks*1024)

    @retry_async(
        retry_on_exceptions=(httpx.HTTPError, httpx.ConnectionClosed),
        max_calls_total=_retry_attempts,
        retry_window_after_first_call_in_seconds=_retry_seconds
    )
    async def create(self, origin, destination, overwrite=False):
        async with httpx.AsyncClient() as session:
            params = {
                'op': 'CREATE',
                    'overwrite': str(overwrite).lower(),
                    'user.name': self._user
                }

            # Kerberos verification
            if self._kerberos_token:
                params = {**params, **{'delegation': self._kerberos_token}}

            hdfs_path = str(self._url / destination)
            response_name_node = await session.put(hdfs_path, params=params, allow_redirects=False)
            response_data_node = await session.put(
                response_name_node.headers['location'],
                data=self._file_sender(file_name=origin),
                params={'delegation': self._kerberos_token},
                timeout=self._timeout_seconds * 60  # In minutes
            )

            return response_data_node

    @retry_async(
        retry_on_exceptions=(httpx.HTTPError, httpx.ConnectionClosed),
        max_calls_total=_retry_attempts,
        retry_window_after_first_call_in_seconds=_retry_seconds
    )
    async def open(self, path):
        async with httpx.AsyncClient() as session:
            params = {
                'op': 'OPEN',
                    'user.name': self._user
                }

            # Kerberos verification
            if self._kerberos_token:
                params = {**params, **{'delegation': self._kerberos_token}}

            hdfs_path = str(self._url / path)
            response_name_node = await session.get(hdfs_path, params=params, allow_redirects=False)
            response_data_node = await session.get(
                response_name_node.headers['location'],
                params={'delegation': self._kerberos_token},
                timeout=self._timeout_seconds * 60  # In minutes
            )

            return response_data_node

    @retry_async(
        retry_on_exceptions=(httpx.HTTPError, httpx.ConnectionClosed),
        max_calls_total=_retry_attempts,
        retry_window_after_first_call_in_seconds=_retry_seconds,
    )
    async def _get_operation(self, path: str, params, key):
        async with httpx.AsyncClient() as session:
            # Kerberos verification
            if self._kerberos_token:
                params = {**params, **{'delegation': self._kerberos_token}}

            hdfs_path = str(self._url / path)
            response_name_node = await session.get(hdfs_path, params=params)
            if response_name_node.status_code == 200:
                body = response_name_node.json()
                if key in body.keys():
                    return body
                elif "RemoteException" in body.keys():
                    raise FileNotFoundError(f'HDFS does not have a reference for {path}.')
            else:
                raise FileNotFoundError(f'HDFS does not have a reference for {path}.')
        
    def get_file_status(self, path):
        params = {
                'op': 'GETFILESTATUS',
                'user.name': self._user
            }
        key = 'FileStatus'
        return self._get_operation(path, params, key)

    def list_directory(self, path):
        params = {
                'op': 'LISTSTATUS',
                'user.name': self._user
            }
        key = 'FileStatuses'
        return self._get_operation(path, params, key)

    def get_content_summary(self, path):
        params = {
                'op': 'GETCONTENTSUMMARY',
                'user.name': self._user
            }
        key = 'ContentSummary'
        return self._get_operation(path, params, key)