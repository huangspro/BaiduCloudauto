from flask import Flask, render_template, request
from src.utils import *


app = Flask(__name__)

@app.route("/apply", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        a = request.form.get("a")
        b = request.form.get("b")
        return f"输入内容：{a}, {b}"

    return render_template("index.html")

app.run(debug=True)



