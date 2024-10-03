from telethon import TelegramClient, events
from settings import api_id, api_hash, phone_number, passw2FA,api_key,api_secret
from pybit.unified_trading import HTTP
import re

# Инициализация клиента с файлом сессии
# Если будет много клиентов, то нужно доработать под разные сессиии и идентификационные данные
client = TelegramClient('user_session', api_id, api_hash, system_version='4.16.30-vxCUSTOM')
channel_id = 1302815576 #для теста используется ТК '@Tatarstan24TV'
passw = passw2FA

# Настройки для Bybit API (демо-счет)
session = HTTP(
    demo=True,
    api_key=api_key,
    api_secret=api_secret,
)

# Функция для извлечения takeProfit и stopLoss из текста сообщения
# Вероятно текст сообщения будет примерно такого характера:
# "Торговый сигнал: покупка BTC/USDT. takeProfit: 60000.000, stopLoss: 61000.000."
# extract_trade_parameters вернет соответственно значения 60000 и 61000,


def extract_trade_parameters(message):
    # Регулярное выражение для поиска takeProfit и stopLoss
    take_profit = re.search(r'takeProfit\s*:\s*(\d+\.?\d*)', message)
    stop_loss = re.search(r'stopLoss\s*:\s*(\d+\.?\d*)', message)

    if take_profit and stop_loss:
        return float(take_profit.group(1)), float(stop_loss.group(1))
    return None, None


async def main():
    print("Проверяем авторизацию пользователя...")
    # Проверяем, подключен ли клиент (сессия сохранена)
    # Подключаемся к Telegram, но не авторизуемся
    await client.connect()

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
        message = event.message.message
        take_profit, stop_loss = extract_trade_parameters(message)
        #print(f'Новое сообщение из канала: {event.message.to_dict()}')
        print(f'Новое сообщение из канала: {message}')

        if take_profit and stop_loss:
            print(f'Получены параметры сделки: TP={take_profit}, SL={stop_loss}')
            # Открытие ордера на Bybit
            try:
                order = session.place_order(
                    category="spot",  # Выбор категории, нужно уточнить
                    symbol="BTCUSDT",  # Символ для торговли – уточнить, где брать или постоянный
                    side="Buy",  # Покупка/Продажа – уточнить, где брать или постоянный
                    order_type="Limit",  # Тип ордера – уточнить, скорее всего Limit (рыночный Market)
                    qty=0.001,  # Количество – уточнить, где брать
                    price=take_profit,
                    triggerPrice=stop_loss,
                    timeInForce="PostOnly",  # уточнить, что ставить
                    isLeverage=0,  # в долг не берем, уточнить
                    orderFilter="tpslOrder",  # tpslOrder: Спотовый ордер TP/SL, активы заняты еще до срабатывания ордера
                )
                # Извлечение данных из ответа
                if order['retCode'] == 0:  # Проверяем, успешный ли ответ
                    order_id = order['result'].get('orderId', 'N/A')
                    order_link_id = order['result'].get('orderLinkId', 'N/A')
                    ret_msg = order.get('retMsg', 'N/A')
                    print(f"Ордер успешно открыт!\nOrder ID: {order_id}\nOrder Link ID: {order_link_id}\nСообщение: {ret_msg}")
                else:
                    print(f"Ошибка при открытии ордера: {order['retMsg']}")

            except Exception as e:
                print(f"Ошибка при открытии ордера: {e}")
        else:
            print('Не удалось извлечь параметры сделки')



try:
    # Явно запускаем клиента и вызываем основную функцию
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
except Exception as e:
    print(f'Произошла ошибка: {e}')
