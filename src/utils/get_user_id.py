import requests
from src.utils.read_token_file import get



url = "https://pan.baidu.com/rest/2.0/xpan/nas"

access_token = get("access_token.txt")

params = {
    "method": "uinfo",
    "access_token": access_token
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

data = response.json()
print(data)
