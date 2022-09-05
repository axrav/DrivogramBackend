"""functions used in the project, database commands simplified made more easier"""
import random
import string

import pyrogram


def data_key(type, len):
    return type + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=len)
    )


## Not using conversion anymore
# def convert_bytes(size):
#     for x in ["bytes", "KB", "MB", "GB", "TB"]:
#         if size < 1024.0:
#             return "%3.1f %s" % (size, x)
#         size /= 1024.0

#     return size


def chunk_stream(client: pyrogram.Client, fileID: str):
    for chunk in client.stream_media(str(fileID)):
        yield chunk
