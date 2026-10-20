class EventBus:
    def __init__(self):
        self.event_list = []

    def raise_event(self, event):
        self.event_list.append(event)

    def handle_event(self):
        for event in self.event_list:
            for handler in self.handler_list:
                handler(event)
