from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, name, data):
        self.name = name
        self.data = data

# raised when transfer successful
class TransferSucceeded(Event):
    def __init__(self, data):
        super().__init__("TransferSucceeded", data)

# raised when transfer failed
class TransferFailed(Event):
    def __init__(self, data):
        super().__init__("TransferFailed", data)