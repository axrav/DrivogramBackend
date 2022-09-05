from pyrogram import Client

from Config.config import config

app1 = Client(
    "app1",
    config.api_id,
    config.api_hash,
    bot_token=config.bot_token1,
)
app2 = Client(
    "app2",
    config.api_id,
    config.api_hash,
    bot_token=config.bot_token2,
)
app3 = Client(
    "app3",
    config.api_id,
    config.api_hash,
    bot_token=config.bot_token3,
)
app4 = Client(
    "app4",
    config.api_id,
    config.api_hash,
    bot_token=config.bot_token4,
)
