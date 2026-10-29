"""
send email to users
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path

import src.event_handler.message_bus as MB
from src.utils.read_token_file import get


TOKEN_DIR = str(Path(__file__).resolve().parent.parent / "token") + "/"








# data should contain \:
# receiver
# message
def send_email(data):
    if not os.path.exists(TOKEN_DIR + "email_password.txt"):
        print("email sending service is not available, please add token/email_password.txt file")
        return

    with open(TOKEN_DIR + "email_password.txt", "r") as f:
        email_setting = f.read().split("\n")
        smtp_server = email_setting[0].split(":")[1].strip()
        smtp_port = email_setting[1].split(":")[1].strip()
        sender = email_setting[2].split(":")[1].strip()
        password = email_setting[3].split(":")[1].strip()


    print("sending email to", data["receiver"])
    message = MIMEText(data["message"], "plain", "utf-8")
    message["From"] = Header(sender, "utf-8")
    message["To"] = Header(data["receiver"], "utf-8")
    message["Subject"] = Header("email message from baiduauto", "utf-8")

    smtp = smtplib.SMTP_SSL(smtp_server, int(smtp_port))
    try:
        smtp.login(sender, password)
        smtp.sendmail(sender, [data["receiver"]], message.as_string())
    except Exception as e:
        print(f"failed to send: {e}")
    finally:
        smtp.quit()


MB.message_bus.subscribe("TransferSucceeded", send_email)
MB.message_bus.subscribe("TransferFailed", send_email)
