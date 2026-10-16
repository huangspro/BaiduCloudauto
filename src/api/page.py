from flask import Flask, render_template, request
from src.utils import *


app = Flask(__name__,  template_folder="html")

@app.route("/apply", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        share_link = request.form.get("share_link")
        share_password = request.form.get("share_password")
        raise_event()

    return render_template("apply.html")

app.run(debug=True)



