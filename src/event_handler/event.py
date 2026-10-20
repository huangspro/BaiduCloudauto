from abc import ABC

class Event(ABC):
    def __init__(self, name):
        self.name = name


class TransferEvent(Event):
    def __init__(self, share_link, password):
        super().__init__("TransferEvent")
        self.share_link = share_link
        self.password = password

class DownlloadEvent(Event):
    def __init__(self, file_name):
        super().__init__("DownloadEvent")
        self.file_name = file_name