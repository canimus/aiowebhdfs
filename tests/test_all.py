from aiowebhdfs import WebHdfsAsyncClient
import pytest
from functools import wraps

config = {  
  'url' : 'https://clrv0000173986.ic.ing.net:8443',
  'user' : 'spark',
  'token' : ''
}


def test_kerberos_decorator():
  client = WebHdfsAsyncClient()

def test_constructor():
  assert True

def test_parameters():
  assert True
  