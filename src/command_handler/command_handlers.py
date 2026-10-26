from pathlib import Path

from src.command_handler.command import *
from src.event_handler.message_bus import message_bus
import src.utils as utils
from src.event_handler.event import *

HANDLERS = []  # storing all the handlers
USER_LINKS = (
    str(Path(__file__).resolve().parent.parent / "user_links") + "/"
)  # the path pointing to "src/user_links/"


# decorator, for adding handler functions to the list HANDLERS
def register_handler(func):
    HANDLERS.append(func)
    return func


# To handle the transfer command
# transfer -> send email to user -> get links
@register_handler
def transfer_command_handler(command_bus, transfer_command):
    path = "/apps/autotool/mydir/" + transfer_command.to_extract_code + "/"
    if transfer_command.name == "TransferCommand":
        print(message_bus.events)
        if utils.transfer_share_link.transfer(
            folder_name=path,
            links=transfer_command.share_link,
            password=transfer_command.password,
        ):
            # raise the transfer successful event
            message_bus.post(TransferSucceeded("文件转存成功"))
            # start get links from baidu cloud
            command_bus.raise_command(
                ReturnLinksCommand(path, transfer_command.to_extract_code)
            )
        else:
            # raise the transfer failed event
            message_bus.post(TransferFailed("文件转存失败"))


# get links from baidu cloud and save it to "src/user_links/to_extract_code.txt"
@register_handler
def return_links_command_handler(command_bus, return_links_command):
    if return_links_command.name == "ReturnLinksCommand":
        # get links here
        file_list = utils.get_fs_id.list_all_files(return_links_command.path)

        result = []

        for i in file_list:
            result.append(utils.get_dlink.get_dlink(i["fs_id"], i["path"]))
            result.append(i["path"].replace("/apps/autotool/mydir/", ""))

        # all the download info will be stored in "{to_extract_code}.txt"
        # line 1: access_token
        # line 2: download link
        # line 3: file path
        # ...
        with open(USER_LINKS + return_links_command.to_extract_code + ".txt", "w") as f:
            f.write(utils.read_token_file.get("access_token.txt"))
            f.write("\n")
            f.write("\n".join(result))
