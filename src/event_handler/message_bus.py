class MessageBus:
    def __init__(self):
        self.events = {}   # storing {event_name1:[subscriber1, subscriber2, subscriber3, ...], ...}
        
    def subscribe(self, event_name, handler):
        if event_name not in self.events.keys():
            self.events[event_name] = handler
        else:
            self.events[event_name].append(handler)
            
    def post(self, event_name, data):
        if event_name in self.events.keys():
            for subscriber in self.events[event_name]:
                subscriber(event_name, data)