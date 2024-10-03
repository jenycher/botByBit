from telethon import TelegramClient, events
from pybit.unified_trading import HTTP
import re


from settings import api_id
from settings import api_hash
from settings import api_key
from settings import api_secret
from settings import bot_token

# Настройки для подключения к Telegram

channel_id = '@Tatarstan24TV'  # ID канала, который вы отслеживаете

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
with channel_id:
    channel_id.loop.run_until_complete(check_channel_type(channel_id))

# Настройки для Bybit API (демо-счет)
#base_url = "https://api-demo.bybit.com",
session = HTTP(
    demo=True,
    api_key=api_key,
    api_secret=api_secret,
)


# Инициализация клиента с токеном бота
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)



# Функция для извлечения takeProfit и stopLoss из текста сообщения
def extract_trade_parameters(message):
    # Регулярное выражение для поиска takeProfit и stopLoss
    take_profit = re.search(r'takeProfit\s*:\s*(\d+\.?\d*)', message)
    stop_loss = re.search(r'stopLoss\s*:\s*(\d+\.?\d*)', message)

    if take_profit and stop_loss:
        return float(take_profit.group(1)), float(stop_loss.group(1))
    return None, None


# Обработка новых сообщений в канале
@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    message = event.message.message
    take_profit, stop_loss = extract_trade_parameters(message)

    if take_profit and stop_loss:
        print(f'Получены параметры сделки: TP={take_profit}, SL={stop_loss}')

        # Открытие ордера на Bybit
        try:
            order = session.place_order(
                category="linear",  # Выбор категории, например, linear для USDT-контрактов
                symbol="BTCUSDT",  # Символ для торговли
                side="Buy",  # Покупка/Продажа
                order_type="Market",  # Тип ордера
                qty=0.01,  # Количество
                takeProfit=take_profit,
                stopLoss=stop_loss,
                timeInForce="GoodTillCancel",
            )
            print(f"Открыт ордер: {order}")
        except Exception as e:
            print(f"Ошибка при открытии ордера: {e}")
    else:
        print('Не удалось извлечь параметры сделки')



# Запуск клиента
client.run_until_disconnected()