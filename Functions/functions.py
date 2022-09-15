"""functions used in the project, database commands simplified made more easier"""
import json
import random
import string

import pyrogram
from cryptography.fernet import Fernet
from pydantic import BaseModel

from Config.config import config

# from Webserver.webserver import Share


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


class Share(BaseModel):
    userkey: str
    filekey: str
    exp: float


def chunk_stream(client: pyrogram.Client, fileID: str):
    for chunk in client.stream_media(str(fileID)):
        yield chunk


async def file_info(client: pyrogram.client, message_id):
    info = await client.get_messages(config.chat_id, message_id)
    return (
        info.document.file_id,
        info.document.file_name,
        info.document.file_size,
        info.document.mime_type,
    )


async def encrypt_and_return(share: Share):
    encrypt_client = Fernet(config.secret_key)
    encrypted = encrypt_client.encrypt(
        str(share.__dict__).encode("utf-8")
    ).decode("utf-8")
    return encrypted


async def decrypt_and_return(enc_token):
    decrypt_client = Fernet(config.secret_key)
    decrypted = (
        decrypt_client.decrypt(token=enc_token.encode("utf-8"))
        .decode("utf-8")
        .replace("'", '"')
    )
    final_data = json.loads(decrypted)
    return final_data
