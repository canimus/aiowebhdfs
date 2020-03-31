# aiowebhdfs

I know, nobody uses `Hadoop` anymore, but for those who do, here is a library that handles large files with `async` features for web requests using the `httpx` library and `aiofiles` for streaming data from __HDFS__

## Features
- Implements retries and timeout windows with `retry_async` from `opnieuw` library
- Implements streaming through the `aiofiles` library
- Implments async requests through the `httpx` library
- Fully tested for core subset of operations in WebHDFS `v3.2.1`

## CREATE = Write File

```python
from aiowebhdfs import WebHdfsAsyncClient
client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
client.create('c:\\temp\\bigfile.txt', '/data/agg/bigfile.txt', overwrite=False)
```

## OPEN = Read File

```python
from aiowebhdfs import WebHdfsAsyncClient
client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
client.open('/data/agg/bigfile.txt')
Content of the file
```

## GETFILESTATUS = File Info

```python
from aiowebhdfs import WebHdfsAsyncClient
client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
client.get_file_status('/data/agg/bigfile.txt')
{
  "FileStatus":
  {
    "accessTime"      : 0,
    "blockSize"       : 0,
    "group"           : "supergroup",
    "length"          : 0,             //in bytes, zero for directories
    "modificationTime": 1320173277227,
    "owner"           : "webuser",
    "pathSuffix"      : "",
    "permission"      : "777",
    "replication"     : 0,
    "type"            : "DIRECTORY"    //enum {FILE, DIRECTORY}
  }
}
```

## LISTSTATUS = List Directory 

```python
from aiowebhdfs import WebHdfsAsyncClient
client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
client.list_directory('/tmp')
{
  "FileStatuses":
  {
    "FileStatus":
    [
      {
        "accessTime"      : 1320171722771,
        "blockSize"       : 33554432,
        "group"           : "supergroup",
        "length"          : 24930,
        "modificationTime": 1320171722771,
        "owner"           : "webuser",
        "pathSuffix"      : "a.patch",
        "permission"      : "644",
        "replication"     : 1,
        "type"            : "FILE"
      },
      {
        "accessTime"      : 0,
        "blockSize"       : 0,
        "group"           : "supergroup",
        "length"          : 0,
        "modificationTime": 1320895981256,
        "owner"           : "szetszwo",
        "pathSuffix"      : "bar",
        "permission"      : "711",
        "replication"     : 0,
        "type"            : "DIRECTORY"
      },
      ...
    ]
  }
}
```

## GETCONTENTSUMMARY = Summary of Directory

```python
from aiowebhdfs import WebHdfsAsyncClient
client = WebHdfsAsyncClient(host='namenode.local', port=8443, user='spark', kerberos_token=token)
client.list_directory('/tmp')
{
  "FileStatuses":
  {
    "FileStatus":
    [
      {
        "accessTime"      : 1320171722771,
        "blockSize"       : 33554432,
        "group"           : "supergroup",
        "length"          : 24930,
        "modificationTime": 1320171722771,
        "owner"           : "webuser",
        "pathSuffix"      : "a.patch",
        "permission"      : "644",
        "replication"     : 1,
        "type"            : "FILE"
      },
      {
        "accessTime"      : 0,
        "blockSize"       : 0,
        "group"           : "supergroup",
        "length"          : 0,
        "modificationTime": 1320895981256,
        "owner"           : "szetszwo",
        "pathSuffix"      : "bar",
        "permission"      : "711",
        "replication"     : 0,
        "type"            : "DIRECTORY"
      },
      ...
    ]
  }
}
```