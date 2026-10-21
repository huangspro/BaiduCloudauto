from src.event_handler.event_handlers import HANDLERS


class EventBus:
    def __init__(self):
        self.event_list = []
        self.is_running = False

    def raise_event(self, event):
        self.event_list.append(event)
        if not self.is_running:
            self.is_running = True
            self.handle_event()

    def handle_event(self):
        for event in self.event_list:
            for handler in HANDLERS:
                if handler(self, event):
                    self.event_list.remove(event)
        self.is_running = False