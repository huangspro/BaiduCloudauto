"""
delete a file from baidu cloud
"""

import json
import requests
from src.utils.read_token_file import get


def delete_file(path):
    access_token = get("access_token.txt")

    url = "https://pan.baidu.com/rest/2.0/xpan/file"
    params = {
        "method": "filemanager",
        "opera": "delete",
        "access_token": access_token,
    }
    headers = {"User-Agent": "pan.baidu.com"}
    data = {
        "async": 0,
        "filelist": json.dumps([path], ensure_ascii=False),
    }

    try:
        response = requests.post(
            url,
            params=params,
            data=data,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()

        return result.get("errno") == 0

    except (requests.RequestException, ValueError):
        return False
