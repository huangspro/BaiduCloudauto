from src.event_handler.event_handlers import HANDLERS


class EventBus:
    def __init__(self):
        self.event_list = []

    def raise_event(self, event):
        self.event_list.append(event)
        self.handle_event()

    def handle_event(self):
        while len(self.event_list) > 0:
            for event in self.event_list:
                for handler in HANDLERS:
                    if handler(self, event):
                        print("handled event", event.name)


    def remove_event(self, event):
        self.event_list.remove(event)