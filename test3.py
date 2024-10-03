from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from settings import api_id
from settings import api_hash
from settings import bot_token

# Инициализация клиента
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
async def get_channel_id():
    channel = await client.get_entity('@Tatarstan24TV')
    print(f"ID канала: {channel.id}")

#with client:
#    client.loop.run_until_complete(get_channel_id())

async def get_messages():
    messages = await client.get_messages('@Tatarstan24TV', limit=10)
    for message in messages:
        print(message.text)

with client:
    client.loop.run_until_complete(get_messages())