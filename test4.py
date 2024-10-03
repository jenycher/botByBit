from telethon import TelegramClient, events
from settings import api_id, api_hash, phone_number

# Инициализация клиента с файлом сессии
client = TelegramClient('user_session', api_id, api_hash)
channel_id = 1302815576
passw = '' #здесь ввести пароль


async def main():
    # Проверяем, подключен ли клиент (сессия сохранена)
    if not await client.is_user_authorized():
        print("Сессия не найдена, выполняем авторизацию...")
        await client.start(phone=phone_number, password=passw)  # Выполняем авторизацию с 2FA
    else:
        print("Сессия уже активна, авторизация не требуется.")

    # Обработка команды /start (если вы планируете запускать через себя)
    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        sender = await event.get_sender()
        await event.respond(f"Привет, {sender.first_name}! Я отслеживаю сообщения канала.")
        print(f"Пользователь {sender.first_name} запустил отслеживание.")

    # Обработка новых сообщений в канале
    @client.on(events.NewMessage(chats=channel_id))
    async def handler(event):
        print(f'Новое сообщение из канала: {event.message.to_dict()}')

    # Запуск клиента для ожидания новых событий
    await client.run_until_disconnected()

# Запуск клиента
with client:
    client.loop.run_until_complete(main())
