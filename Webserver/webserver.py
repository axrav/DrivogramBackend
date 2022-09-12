import os
import sys
import time

from cryptography.fernet import Fernet

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import asyncio
import json
import random
from io import BytesIO

import auth
import jwt
import pytz
import uvicorn
from Crypto.Cipher import AES
from fastapi import (Depends, FastAPI, Header, HTTPException,
                     UploadFile)
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security.api_key import APIKey
from pydantic import BaseModel

from Database.db import database
from Functions.functions import chunk_stream, data_key

data_object = database()
import nest_asyncio
from pyrogram import idle

from Config.config import config
from Telegram.client import app1, app2, app3, app4

chat_id = config.chat_id
choose = [app1, app2, app3, app4]
nest_asyncio.apply()
web = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

web.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@web.on_event("startup")
async def startup():
    async def client_start():
        await app1.start()
        await app2.start()
        await app3.start()
        await app4.start()
        await idle()

    asyncio.create_task(client_start())


@web.post("/api/upload")
async def home(
    IN_FILE: UploadFile, X_API_KEY: APIKey = Depends(auth.apikey)
):
    content = await IN_FILE.read()
    b = BytesIO(content)
    b.name = IN_FILE.filename
    random_client = random.choice(choose)
    data_object.create_file_table(table_name="FileData")
    key_file = data_key(type="FILE-", len=7)
    doc = await random_client.send_document(
        chat_id, b, force_document=True, caption=f"{key_file}"
    )
    data_object.insert_file_data(
        filename=IN_FILE.filename,
        fileSize=str(doc.document.file_size),
        MessageID=doc.id,
        FileKey=key_file,
        UserID=X_API_KEY,
        Content=IN_FILE.content_type,
        Time=doc.date,
    )
    return JSONResponse(
        status_code=200,
        content={
            "msg": "file uploaded successfully",
            "file_key": key_file,
            "user": X_API_KEY,
        },
    )


@web.get("/api/signup")
async def data(NAME: str | None = Header(default=None)):
    data_object.create_user_table("UserData")
    if NAME == None or NAME == "":
        raise HTTPException(
            status_code=422,
            detail="missing parameter 'NAME',provide a name",
        )
    return JSONResponse(
        {"X-API-KEY": data_object.add_user(NAME)}, status_code=200
    )


@web.get("/api/logincheck")
async def login(X_API_KEY: str | None = Header(default=None)):
    if X_API_KEY == None:
        raise HTTPException(
            status_code=422,
            detail="NO X-API KEY PROVIDED UNABLE TO PROCEED",
        )
    x = data_object.login_check(X_API_KEY)
    if x == None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized Login, Please signup",
        )
    return JSONResponse(
        status_code=200,
        content={
            "login": True,
            "user": x,
        },
    )


@web.get("/api/uploads")
async def uploads(X_API_KEY: APIKey = Depends(auth.apikey)):
    return JSONResponse(
        status_code=200,
        content={
            "User": X_API_KEY,
            "Uploads": data_object.get_uploads(X_API_KEY),
        },
    )


@web.delete("/api/delete")
async def delete(
    FILE_KEY: str | None = Header(default=None),
    X_API_KEY: APIKey = Depends(auth.apikey),
):
    name = data_object.deleteFile(FILE_KEY, X_API_KEY)
    if name == None:
        raise HTTPException(status_code=404, detail="File Not Found")
    return JSONResponse(
        status_code=200,
        content={
            "user": X_API_KEY,
            "file": name,
            "message": "Deleted the file successfully",
        },
    )


@web.get("/api/download")
async def download(
    FILE_KEY: str | None = Header(default=None),
    X_API_KEY: APIKey = Depends(auth.apikey),
):
    if FILE_KEY == None or FILE_KEY == "":
        raise HTTPException(
            status_code=404, detail="Invalid file Key"
        )
    message_id = data_object.getFile(
        file_key=FILE_KEY, User_id=X_API_KEY
    )
    if message_id == None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        random_client = random.choice(choose)
        msg = await random_client.get_messages(chat_id, message_id)
        file_id = msg.document.file_id
        file_size = msg.document.file_size
        file_name = msg.document.file_name
        file_content = msg.document.mime_type
        stream_data = chunk_stream(
            client=random_client, fileID=file_id
        )
    return StreamingResponse(
        stream_data,
        status_code=200,
        media_type=file_content,
        headers={
            "content-length": str(file_size),
            "X-FILE-NAME": file_name,
        },
    )


class Share(BaseModel):
    userkey: str
    filekey: str
    exp: float


@web.post("/api/share")
async def sharable(
    share: Share,
    X_API_KEY: APIKey = Depends(auth.apikey)
):  # )
    share.exp = int(time.time()) + share.exp*3600
    token = jwt.encode(payload=share.__dict__, key=config.jwt_secret)
    encrypt_client = Fernet(config.jwt_secret)
    encrypted = encrypt_client.encrypt(token.encode("utf-8"))
    return JSONResponse(
        status_code=200,
        content={"link" : f"drivogram.aaravarora.in/share/?token={encrypted}"}
        )


@web.get("/share/")
async def share(token: str):
    decrypt_client = Fernet(config.jwt_secret)
    decrypted = decrypt_client.decrypt(token=token).decode("utf-8")
    try:
        data = jwt.decode(
            decrypted, algorithms=["HS256"], key=config.jwt_secret
        )
        message_id = data_object.getFile(
            file_key=data["filekey"], User_id=data["userkey"]
        )
        if message_id == None:
            raise HTTPException(status_code=404, detail="Not Found")
        else:
            random_client = random.choice(choose)
            msg = await random_client.get_messages(
                chat_id, message_id
            )
            file_id = msg.document.file_id
            file_size = msg.document.file_size
            file_name = msg.document.file_name
            file_content = msg.document.mime_type
            stream_data = chunk_stream(
                client=random_client, fileID=file_id
            )
            return StreamingResponse(
                stream_data,
                status_code=200,
                media_type=file_content,
                headers={
                    "content-length": str(file_size),
                    "X-FILE-NAME": file_name,
                },
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=503, detail="The sharing session has expired"
        )


uvicorn.run(web, port=config.web_port)
