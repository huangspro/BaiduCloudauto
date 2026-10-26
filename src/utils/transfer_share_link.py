"""
transfer files and folders from a share link to my cloud
"""

from src.transfer.operations import Operation
from src.utils.read_token_file import get
from pathlib import Path


def transfer(folder_name: str = "/", links: str = "", password: str = ""):
    return Operation().save(
        cookie=get("cookie.txt"),
        folder_name=folder_name,
        trust_env=True,
        custom_mode=False,
        check_mode=False,
        links=links + "?pwd=" + password,
        on_status=lambda *a: None,
        on_log=print,
    )
