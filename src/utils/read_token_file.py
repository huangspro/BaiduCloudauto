"""
read text content from a txt file in src/token/
"""


import sys
from pathlib import Path


TOKEN_DIR = str(Path(__file__).resolve().parent.parent / "token") + "/"

def get(path):
    with open(TOKEN_DIR + path, "r", encoding="utf-8") as f:
        value = f.read().strip()
        if value == "":
            print(f"{TOKEN_DIR + path} is empty")
            sys.exit(1)
        return value
        

