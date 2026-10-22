import os

from flask import Flask, render_template, request
from src.utils import *
from src.event_handler import event_bus, event

import sys
from pathlib import Path
from src.utils.read_token_file import get

app = Flask(__name__,  template_folder="html")
event_bus = event_bus.EventBus()
USER_LINKS = str(Path(__file__).resolve().parent.parent / "user_links") + "/"


@app.route("/apply", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        share_link = request.form.get("share_link")
        share_password = request.form.get("share_password")
        to_extract_code = request.form.get("to_extract_code")

        new_event = event.TransferEvent(share_link, share_password, to_extract_code)
        event_bus.raise_event(new_event)

    return render_template("apply.html")


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        to_extract_code = request.values.get("to_extract_code")

        file_path = USER_LINKS + str(to_extract_code) + ".txt"
        if not os.path.exists(file_path):
            return "提取码不存在"

        with open(file_path, "r") as f:
            links = f.read()

        return get("access_token.txt") + "\n" + links
    else:
        return "请使用GET请求"
app.run(debug=True)



