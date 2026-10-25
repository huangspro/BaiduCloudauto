from pathlib import Path

from src.command_handler.command import *
from src.event_handler.message_bus import message_bus
import src.utils.transfer_share_link as transfer_share_link
import src.utils.get_fs_id as get_fs_id
import src.utils.get_dlink as get_dlink
from src.utils.read_token_file import get



HANDLERS = []  # storing all the handlers
USER_LINKS = str(Path(__file__).resolve().parent.parent / "user_links") + "/"  # the path pointing to "src/user_links/"



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
        if transfer_share_link.transfer(folder_name=path,links=transfer_command.share_link,password=transfer_command.password):
            print("transfer successful")
            message_bus.post("TRANSFER_SUCCEED", data = "文件转存成功")
            command_bus.raise_command(ReturnLinksCommand(path, transfer_command.to_extract_code))
        else:
            print("transfer failed")
            message_bus.post("TRANSFER_FAILED", data="文件转存失败")
        print("handled ", transfer_command.name)




# get links from baidu cloud and save it to "src/user_links/to_extract_code.txt"
@register_handler
def return_links_command_handler(command_bus, return_links_command):
    if return_links_command.name == "ReturnLinksCommand":
        # get links here
        file_list = get_fs_id.list_all_files(return_links_command.path)

        result = []

        for i in file_list:
            result.append(get_dlink.get_dlink(i["fs_id"], i["path"]))
            result.append(i["path"].replace("/apps/autotool/mydir/", ""))

        with open(USER_LINKS + return_links_command.to_extract_code + ".txt", "w") as f:
            f.write(get("access_token.txt"))
            f.write("\n")
            f.write("\n".join(result))
    print("handled ", return_links_command.name)