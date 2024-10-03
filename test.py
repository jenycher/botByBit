from telethon import TelegramClient, events

from settings import api_id
from settings import api_hash
from settings import bot_token

# Настройки для подключения к Telegram
#channel_id = '@Tatarstan24TV'  # ID канала, который вы отслеживаете
channel_id=1302815576

# Инициализация клиента с токеном бота
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Обработка команды /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    sender = await event.get_sender()
    await event.respond(f"Привет, {sender.first_name}! Я бот, отслеживающий канал {channel_id}.")
    print(f"Пользователь {sender.first_name} запустил бота.")

@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    print(f'Новое событие: {event.message.to_dict()}')

# Обработка новых сообщений в канале
#@client.on(events.NewMessage(chats=channel_id))
#async def handler(event):
#    message = event.message.message
#    print(f'Сообщение из канала: {message}')


# Запуск клиента
client.run_until_disconnected()
