import json
import os
from datetime import datetime

LOG_PATH = "data/log.json"

def log_event(user: str, message: str):
    """
    Логує подію у файл JSON з часовою позначкою, користувачем та текстом повідомлення.
    Якщо файл пошкоджений або відсутній — створює новий.
    :param user: Ім'я користувача, наприклад, "Користувач" або "Antony"
    :param message: Текст повідомлення або події
    """
    # Перевіряємо чи існує файл і зчитуємо існуючі логи
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    # Формуємо новий запис логу
    new_entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "user": user,
        "message": message
    }
    logs.append(new_entry)

    # Записуємо оновлений список назад у файл
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# Тестовий запуск, можна прибрати в продакшені
if __name__ == "__main__":
    log_event("Тестовий Користувач", "Це тестове повідомлення для логу.")
    print("Лог додано.")