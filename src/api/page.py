from flask import Flask, render_template, request
from src.utils import *
from src.event_handler import event_bus, event

app = Flask(__name__,  template_folder="html")
event_bus = event_bus.EventBus()

@app.route("/apply", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        share_link = request.form.get("share_link")
        share_password = request.form.get("share_password")
        to_extract_code = request.form.get("to_extract_code")
        print(share_link, share_password)

        new_event = event.TransferEvent(share_link, share_password)
        event_bus.raise_event(new_event)

    return render_template("apply.html")

app.run(debug=True)



