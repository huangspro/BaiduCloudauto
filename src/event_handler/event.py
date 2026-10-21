from abc import ABC

class Event(ABC):
    def __init__(self, name):
        self.name = name


class TransferEvent(Event):
    def __init__(self, share_link, password, to_extract_code):
        super().__init__("TransferEvent")
        self.share_link = share_link
        self.password = password
        self.to_extract_code = to_extract_code

class DownloadEvent(Event):
    def __init__(self, file_name):
        super().__init__("DownloadEvent")
        self.file_name = file_name

class ReturnLinksEvent(Event):
    def __init__(self, file_name, path:list, to_extract_code):
        super().__init__("ReturnLinksEvent")
        self.path = path
        self.to_extract_code = to_extract_code