import requests
import sys
from read_token_file import get


def file_metas(access_token, fsids, path):
    url = "https://pan.baidu.com/rest/2.0/xpan/multimedia"

    params = {
        "method": "filemetas",
        "access_token": access_token,
        "fsids": __import__("json").dumps(fsids),
        "dlink": 1,
        "path": path,
        "thumb": 1,
        "needmedia": 1,
        "extra": 1
    }

    headers = {
        "Host": "pan.baidu.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "pan.baidu.com"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()

        if data.get("errno") != 0:
            raise RuntimeError(
                f"call filemetas failed: {data}"
            )

        return data

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        sys.exit(1)

    except ValueError:
        print("Invalid JSON response:", response.text)
        sys.exit(1)


if __name__ == "__main__":
    access_token = get("../token/access_token.txt")

    fsids = [901185618239706]
    path = "/apps/autotool/mydir/ok.epub"

    data = file_metas(access_token, fsids, path)

    print("完整返回数据:")
    print(data)

    files = data.get("list", [])

    for file_info in files:
        print("filename:", file_info.get("filename") or file_info.get("server_filename"))
        print("fs_id:", file_info.get("fs_id"))
        print("dlink:", file_info.get("dlink"))
