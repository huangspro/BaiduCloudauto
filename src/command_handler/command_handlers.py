import sys
from pathlib import Path

from src.command_handler.command import *

import src.utils.transfer_share_link as transfer_share_link
import src.utils.download as download
import src.utils.get_fs_id as get_fs_id
import src.utils.get_dlink as get_dlink
from src.utils.read_token_file import get


HANDLERS = []
USER_LINKS = str(Path(__file__).resolve().parent.parent / "user_links") + "/"

def register_handler(func):
    HANDLERS.append(func)
    return func


@register_handler
def transfer_command_handler(command_bus, transfer_command) -> bool:
    path = "/apps/autotool/mydir/" + transfer_command.to_extract_code + "/"
    if transfer_command.name == "TransferCommand":
        transfer_share_link.transfer(folder_name=path,links=transfer_command.share_link,password=transfer_command.password)
        command_bus.remove_command(transfer_command)

        command_bus.raise_command(ReturnLinksCommand(path, transfer_command.to_extract_code))
        return True
    else:
        return False

@register_handler
def download_command_handler(command_bus, download_command) -> bool:
    if download_command.name == "DownloadCommand":
        return True
    else:
        return False


@register_handler
def return_links_command_handler(command_bus, return_links_command) -> bool:
    print("begin getting links")
    if return_links_command.name == "ReturnLinksCommand":
        file_list = get_fs_id.list_all_files(return_links_command.path)

        result = []

        for i in file_list:
            result.append(get_dlink.get_dlink(i["fs_id"], i["path"]))
            result.append(i["path"].replace("/apps/autotool/mydir/", ""))

        with open(USER_LINKS + return_links_command.to_extract_code + ".txt", "w") as f:
            f.write(get("access_token.txt"))
            f.write("\n")
            f.write("\n".join(result))
            print("saved to file", return_links_command.to_extract_code, ".txt")

        command_bus.remove_command(return_links_command)
        return True
    else:
        return False