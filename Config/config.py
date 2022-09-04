from os import getenv as ge

from dotenv import load_dotenv

load_dotenv()


class config:
    chat_id = int(ge("CHAT_ID"))
    api_id = int(ge("API_ID"))
    api_hash = ge("API_HASH")
    bot_token1 = ge("BOT_TOKEN1")
    bot_token2 = ge("BOT_TOKEN2")
    bot_token3 = ge("BOT_TOKEN3")
    bot_token4 = ge("BOT_TOKEN4")
    web_port = int(ge("WEB_PORT"))
    db_name = ge("DB_NAME")
    db_host = ge("DB_HOST")
    db_port = ge("DB_PORT")
    db_user = ge("DB_USER")
    db_password = ge("DB_PASSWORD")
