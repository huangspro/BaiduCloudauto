import os

from flask import Flask, render_template, request
from src.utils import *
from src.command_handler import command_bus, command

import sys
from pathlib import Path
from src.utils.read_token_file import get

app = Flask(__name__,  template_folder="html")
command_bus = command_bus.CommandBus()
USER_LINKS = str(Path(__file__).resolve().parent.parent / "user_links") + "/"


@app.route("/apply", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        share_link = request.form.get("share_link")
        share_password = request.form.get("share_password")
        to_extract_code = request.form.get("to_extract_code")

        new_command = command.TransferCommand(share_link, share_password, to_extract_code)
        command_bus.raise_command(new_command)

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

        return links
    else:
        return "请使用GET请求"

app.run(host="0.0.0.0", port=5000, debug=True)



