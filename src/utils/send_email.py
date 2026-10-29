"""
send email to users
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import src.event_handler.message_bus as MB
from src.utils.read_token_file import get

smtp_server = "smtp.163.com"
smtp_port = 465
sender = "13612276628@163.com"
password = get("email_password.txt")


# data should contain \:
# receiver
# message
def send_email(data):
    print("sending email to", data["receiver"])
    message = MIMEText(data["message"], "plain", "utf-8")
    message["From"] = Header(sender, "utf-8")
    message["To"] = Header(data["receiver"], "utf-8")
    message["Subject"] = Header("email message from baiduauto", "utf-8")

    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    try:
        smtp.login(sender, password)
        smtp.sendmail(sender, [data["receiver"]], message.as_string())
    except Exception as e:
        print(f"failed to send: {e}")
    finally:
        smtp.quit()


MB.message_bus.subscribe("TransferSucceeded", send_email)
MB.message_bus.subscribe("TransferFailed", send_email)
