from aiowebhdfs import WebHdfsAsyncClient
import asyncio
import pytest
import httpx
from unittest.mock import patch

@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

endpoint = 'https://token/generation'
auth = 'actual_token'

@pytest.mark.parametrize('attribute_name', ['_retry_seconds', '_retry_attempts'])
def test_class_attributes(attribute_name):
  assert hasattr(WebHdfsAsyncClient, attribute_name)

@pytest.mark.parametrize('attribute_name', ['_host', '_port', '_user', '_transport', '_endpoint', '_api_version', '_kilobyte_chunks', '_timeout_seconds', '_kerberos_token'])
def test_attributes(attribute_name):
  client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark')
  assert hasattr(client, attribute_name)

def test_create(event_loop):
  headers = httpx.Headers({'Authorization' : auth})
  with httpx.Client() as s:
    token = s.get(endpoint, headers=headers).json()['delegationToken']
    client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
    response = event_loop.run_until_complete(client.create("d:\\aiowebhdfs\\tests\\fixtures\\uno.txt", "/tmp/dos.txt", True))
    assert response.status_code == 201

def test_get_file_status(event_loop):
  headers = httpx.Headers({'Authorization' : auth})
  with httpx.Client() as s:
    token = s.get(endpoint, headers=headers).json()['delegationToken']
    client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
    response = event_loop.run_until_complete(client.get_file_status("/tmp/dos.txt"))
    assert response['FileStatus']['type'] == 'FILE'
