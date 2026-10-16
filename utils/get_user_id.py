import requests
from read_token_file import get

url = "https://pan.baidu.com/rest/2.0/xpan/nas"

access_token = get("../token/access_token.txt")

params = {
    "method": "uinfo",
    "access_token": access_token
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

data = response.json()
print(data)
