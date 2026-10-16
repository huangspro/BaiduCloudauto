import requests
import sys
from read_token_file import get

url = "https://pan.baidu.com/rest/2.0/xpan/file"

access_token = get("../token/access_token.txt")

params = {
    "method": "list",
    "dir": "/apps/autotool/mydir",
    "order": "time",
    "start": 0,
    "limit": 10,
    "web": 1,
    "folder": 0,
    "access_token": access_token,
    "desc": 1
}

headers = {
    "User-Agent": "pan.baidu.com"
}

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=15
)
response.raise_for_status()
data = response.json()

if data.get("errno", 0) != 0:
    print("request failed:", data)
    sys.exit(1)


    
file_list = data.get("list", [])

for item in file_list:
    print("filename:", item.get("server_filename"))
    print("path:", item.get("path"))
    print("size:", item.get("size"), "bytes")
    print("fs_id:", item.get("fs_id"))
    print("md5:", item.get("md5"))
    print("is_folder:", bool(item.get("isdir")))
    print("-" * 40)
