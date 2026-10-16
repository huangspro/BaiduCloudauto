import requests
import sys
from read_token_file import get

url = "https://openapi.baidu.com/oauth/2.0/token"

authorization_code = get("../token/authorization_code.txt")
appid = get("../token/appid.txt")
appkey = get("../token/appkey.txt")
secretid = get("../token/secretkey.txt")

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

with open("../token/access_token.txt", "w", encoding="utf-8") as f:
    f.write(access_token)

with open("../token/refresh_token.txt", "w", encoding="utf-8") as f:
    f.write(refresh_token)
