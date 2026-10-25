from src.event_handler.message_bus import message_bus


# decorator, add subscribers to message_bus
def register_handler(event_name):
    def decorator(func):
        message_bus.subscribe(event_name, func)
        return func

    return decorator


@register_handler("transfer_succeed")
@register_handler("transfer_failed")
def send_email(data):
    print("sending email to user")

