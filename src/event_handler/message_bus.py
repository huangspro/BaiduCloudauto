import queue
import threading


class MessageBus:
    def __init__(self):
        self.event_queue = queue.Queue()  # storing all events, their handlers are in HANDLERS
        # the message bus works in a sun thread
        self.worker = threading.Thread(target=self.handle_events, name="EventBusWorker", daemon=True)
        self.events = {}  # storing {event_name1:[subscriber1, subscriber2, subscriber3, ...], ...}
        self.worker.start()

    # subscribe event to message bus
    def subscribe(self, event_name, handler):
        if event_name not in self.events.keys():
            self.events[event_name] = []

        self.events[event_name].append(handler)

    # add an event to event queue
    def post(self, event):
        self.event_queue.put(event)

    # put None into the event queue
    def end_event_handler(self):
        self.event_queue.put(None)

    # running in a sub thread, broadcast events to all subscribers
    def handle_events(self):
        while True:
            # get() function will block the thread until the queue is not empty
            event = self.event_queue.get()

            if event is None:
                return

            if event.name in self.events.keys():
                for subscriber in self.events[event.name]:
                    subscriber(event.data)

# instantiate a message bus as a global bus
message_bus = MessageBus()
