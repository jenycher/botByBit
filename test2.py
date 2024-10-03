from telethon.sync import TelegramClient

# Настройки Telegram API

from settings import api_id
from settings import api_hash
from settings import bot_token

# Инициализация клиента
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

async def check_channel_type(channel_id):
    entity = await client.get_entity(channel_id)
    if entity.broadcast:
        print("Это канал.")
        if entity.username:
            print("Канал публичный.")
        else:
            print("Канал приватный.")
    else:
        print("Это не канал.")

# Проверка канала
with client:
    client.loop.run_until_complete(check_channel_type(1302815576))
#@Tatarstan24TV