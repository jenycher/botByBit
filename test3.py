import re
# Функция для извлечения takeProfit и stopLoss из текста сообщения
def extract_trade_parameters(message):
    # Регулярное выражение для поиска takeProfit и stopLoss
    take_profit = re.search(r'takeProfit\s*:\s*(\d+\.?\d*)', message)
    stop_loss = re.search(r'stopLoss\s*:\s*(\d+\.?\d*)', message)

    if take_profit and stop_loss:
        return float(take_profit.group(1)), float(stop_loss.group(1))
    return None, None


message = "Торговый сигнал: покупка EUR/USD. takeProfit: 1.2500, stopLoss: 1.2000."

# Вызов функции с примерным сообщением
take_profit, stop_loss = extract_trade_parameters(message)

# Вывод результатов
print("Take Profit:", take_profit)
print("Stop Loss:", stop_loss)