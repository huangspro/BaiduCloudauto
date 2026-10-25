import src.event_handler.message_bus as MB


def send_email(data):
    print("sending email to user")

MB.message_bus.subscribe("TRANSFER_SUCCEED", send_email)
MB.message_bus.subscribe("TRANSFER_FAILED", send_email)