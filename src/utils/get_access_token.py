"""
get access_token based on the authorization code
and store the access_token to src/token/access_token.txt
"""


import requests
import sys
from src.utils.read_token_file import get


url = "https://openapi.baidu.com/oauth/2.0/token"

authorization_code = get("authorization_code.txt")
appid = get("appid.txt")
appkey = get("appkey.txt")
secretid = get("secretkey.txt")

params = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "client_id": appkey,
    "client_secret": secretid,
    "redirect_uri": "oob"
}



response = requests.get(url, params=params, timeout=15)
data = response.json()
if "access_token" not in data or "refresh_token" not in data:
    print("failed, sth went wrong")
    sys.exit(1)
    
access_token = data["access_token"]
refresh_token = data["refresh_token"]

with open("access_token.txt", "w", encoding="utf-8") as f:
    f.write(access_token)

with open("refresh_token.txt", "w", encoding="utf-8") as f:
    f.write(refresh_token)
