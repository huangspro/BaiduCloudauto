import os
from flask import Flask, render_template, request
from src.command_handler import command
from src.command_handler.command_bus import command_bus

from pathlib import Path


app = Flask(__name__,  template_folder="html")
USER_LINKS = str(Path(__file__).resolve().parent.parent / "user_links") + "/"


# for user applying transferring
@app.route("/apply", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get data from html page
        share_link = request.form.get("share_link")
        share_password = request.form.get("share_password")
        to_extract_code = request.form.get("to_extract_code")
        email = request.form.get("email")

        # send command to command bus, start transferring
        new_command = command.TransferCommand(share_link, share_password, to_extract_code, email)
        command_bus.raise_command(new_command)

    return render_template("apply.html")


# return download links to users
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



