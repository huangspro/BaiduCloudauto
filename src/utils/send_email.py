"""
send email to users
"""


import src.event_handler.message_bus as MB


def send_email(data):
    print("sending email to user", data)

MB.message_bus.subscribe("TransferSucceeded", send_email)
MB.message_bus.subscribe("TransferFailed", send_email)