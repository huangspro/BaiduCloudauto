import src.utils.transfer_share_link as transfer_share_link
import src.utils.download as download


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


@register_handler
def download_event_handler(download_event):
    if download_event.name == "DownloadEvent":
        pass