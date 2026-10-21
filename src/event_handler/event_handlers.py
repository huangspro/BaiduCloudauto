import src.utils.transfer_share_link as transfer_share_link
import src.utils.download as download
import src.utils.get_fs_id as get_fs_id
import src.utils.get_dlink as get_dlink

HANDLERS = []


def register_handler(func):
    HANDLERS.append(func)
    return func


@register_handler
def transfer_event_handler(transfer_event):
    if transfer_event.name == "TransferEvent":
        transfer_share_link.transfer(
            folder_name="apps/autotool/mydir/",
            links=transfer_event.share_link,
            password=transfer_event.password,
        )

        return "transfer successful"
    else:
        return False

@register_handler
def download_event_handler(download_event):
    if download_event.name == "DownloadEvent":
        pass


@register_handler
def return_links_event_handler(return_links_event):
    if return_links_event.name == "ReturnLinksEvent":
        file_list = get_fs_id.list_all_files(return_links_event.path)

        result = []
        for i in file_list:
            result.append(get_dlink.get_dlink(i["fs_id"], i["path"]))
        return result
    else:
        return False