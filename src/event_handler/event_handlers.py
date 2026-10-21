import sys
from pathlib import Path

from src.event_handler.event import *

import src.utils.transfer_share_link as transfer_share_link
import src.utils.download as download
import src.utils.get_fs_id as get_fs_id
import src.utils.get_dlink as get_dlink

HANDLERS = []
USER_LINKS = str(Path(__file__).resolve().parent.parent / "user_links") + "/"

def register_handler(func):
    HANDLERS.append(func)
    return func


@register_handler
def transfer_event_handler(event_bus, transfer_event) -> bool:
    path = "/apps/autotool/mydir/" + transfer_event.to_extract_code + "/"
    if transfer_event.name == "TransferEvent":
        if transfer_share_link.transfer(folder_name=path,links=transfer_event.share_link,password=transfer_event.password,):
            event_bus.raise_event(ReturnLinksEvent(path, transfer_event.to_extract_code))
        else:
            return False
        return True
    else:
        return False

@register_handler
def download_event_handler(event_bus, download_event) -> bool:
    if download_event.name == "DownloadEvent":
        return True
    else:
        return False


@register_handler
def return_links_event_handler(event_bus, return_links_event) -> bool:
    if return_links_event.name == "ReturnLinksEvent":
        file_list = get_fs_id.list_all_files(return_links_event.path)

        result = []
        for i in file_list:
            result.append(get_dlink.get_dlink(i["fs_id"], i["path"]))

        with open(return_links_event.to_extract_code + ".txt", "w") as f:
            f.write("\n".join(result))

        return True
    else:
        return False