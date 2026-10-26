"""
refresh access token by the refresh_token
and then store the new access_token and refresh_token to files
"""

import requests
import sys
from src.utils.read_token_file import get

url = "https://openapi.baidu.com/oauth/2.0/token"


access_token = get("access_token.txt")
refresh_token = get("refresh_token.txt")
appid = get("appid.txt")
appkey = get("appkey.txt")
secretid = get("secretkey.txt")

params = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token,
    "client_id": appkey,
    "client_secret": secretid,
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()
data = response.json()

if "access_token" not in data or "refresh_token" not in data:
    print("request failed")
    sys.exit(1)

access_token = data["access_token"]
refresh_token = data["refresh_token"]

with open("access_token.txt", "w", encoding="utf-8") as f:
    f.write(access_token)

with open("refresh_token.txt", "w", encoding="utf-8") as f:
    f.write(refresh_token)
