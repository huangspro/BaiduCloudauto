from abv import ABC, abstract

class Event(ABC):
    def __init__(self, name):
        self.name = name
