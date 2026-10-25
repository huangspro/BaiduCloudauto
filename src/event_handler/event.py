from abc import ABC

class Event(ABC):
    def __init__(self, name):
        self.name = name