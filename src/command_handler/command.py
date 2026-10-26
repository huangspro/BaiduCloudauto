from abc import ABC


class Command(ABC):
    def __init__(self, name):
        self.name = name


# start transferring
class TransferCommand(Command):
    def __init__(self, share_link, password, to_extract_code, email):
        super().__init__("TransferCommand")
        self.share_link = share_link
        self.password = password
        self.to_extract_code = to_extract_code
        self.email = email


# no use
class DownloadCommand(Command):
    def __init__(self, file_name):
        super().__init__("DownloadCommand")
        self.file_name = file_name


# command of returning links
class ReturnLinksCommand(Command):
    def __init__(self, path: list, to_extract_code):
        super().__init__("ReturnLinksCommand")
        self.path = path
        self.to_extract_code = to_extract_code


# This Command is to delete expired information such as expired cloud disk files and local users files.
class ExpiredInfoCommand(Command):
    def __init__(self):
        super().__init__("ExpiredInfoCommand")
