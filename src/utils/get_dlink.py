import json
import requests
from read_token_file import get


def get_dlink(fs_id, path):
    access_token = get("../token/access_token.txt")'
    
    # Configure the file metadata request.
    url = "https://pan.baidu.com/rest/2.0/xpan/multimedia"
    params = {
        "method": "filemetas",
        "access_token": access_token,
        "fsids": json.dumps([fs_id]),
        "dlink": 1,
        "path": path,
        "thumb": 1,
        "needmedia": 1,
        "extra": 1,
    }
    headers = {"User-Agent": "pan.baidu.com"}

    # Request file metadata and return the download link.
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("errno") != 0:
            return None

        files = data.get("list", [])
        return files[0].get("dlink") if files else None

    except (requests.RequestException, ValueError):
        return None
        
