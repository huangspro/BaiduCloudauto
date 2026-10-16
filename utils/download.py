import requests
import sys
from read_token_file import get

access_token = get("../token/access_token.txt")

response = requests.get(
    "https://d.pcs.baidu.com/file/6cb06943bl9042fb4e1affebf994a738?fid=1103781937522-250528-901185618239706&rt=pr&sign=FDtAERK-DCb740ccc5511e5e8fedcff06b081203-jYGOfnPGsyQj1mIwG5VY4F8Oeyo%3D&expires=8h&chkbd=0&chkv=0&dp-logid=115302435783167661&dp-callid=0&dstime=1792119201&r=527080331&vuk=1103781937522&origin_appid=124475457&file_type=0",
    params={"access_token": access_token},
    headers={"User-Agent": "pan.baidu.com"},
    stream=True,
    timeout=60,
)
response.raise_for_status()
with open("<FILE_NAME>", "wb") as output:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            output.write(chunk)
