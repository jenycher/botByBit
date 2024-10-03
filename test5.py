from telethon import TelegramClient, events
from pybit.unified_trading import HTTP
from settings import api_id, api_hash, phone_number, passw2FA,api_key,api_secret
import re


# Настройки для Bybit API (демо-счет)

session = HTTP(
    demo=True,
    api_key=api_key,
    api_secret=api_secret,
)


# Открытие ордера на Bybit
try:
    order = session.place_order(
        category="spot",  # Выбор категории, нужно уточнить
        symbol="BTCUSDT",  # Символ для торговли – уточнить, где брать или постоянный
        side="Buy",  # Покупка/Продажа – уточнить, где брать или постоянный
        order_type="Limit",  # Тип ордера – уточнить, скорее всего Limit (рыночный Market)
        qty=0.001,  # Количество – уточнить, где брать
        price=63000,
        triggerPrice=64000,
        timeInForce="PostOnly", #уточнить, что ставить
        isLeverage=0, # в долг не берем, уточнить
        orderFilter="tpslOrder", #tpslOrder: Спотовый ордер TP/SL, активы заняты еще до срабатывания ордера
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


