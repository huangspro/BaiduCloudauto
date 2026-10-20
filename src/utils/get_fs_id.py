import requests
from src.utils.read_token_file import get


def list_files(path: str) -> list[dict]:
    # Read the Baidu Netdisk access token.
    access_token = get("access_token.txt")

    # Configure the directory listing request.
    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    params = {
        "method": "list",
        "dir": path,
        "order": "time",
        "start": 0,
        "limit": 10,
        "web": 1,
        "folder": 0,
        "access_token": access_token,
        "desc": 1,
    }
    headers = {"User-Agent": "pan.baidu.com"}

    # Send the request and validate the response.
    response = requests.get(url, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data.get("errno", 0) != 0:
        raise RuntimeError(f"Baidu Netdisk API error: {data}")

    # Return file metadata as a list of dictionaries.
    return [
        {
            "filename": item.get("server_filename"),
            "path": item.get("path"),
            "size": item.get("size"),
            "fs_id": item.get("fs_id"),
            "md5": item.get("md5"),
            "is_folder": bool(item.get("isdir")),
        }
        for item in data.get("list", [])
    ]
    
    

