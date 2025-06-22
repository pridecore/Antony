import time
from datetime import datetime
import os
import json

LOG_PATH = "data/log.json"

_last_input_time = 0
_last_user_input = ""

def log_user_input(text: str):
    """
    Логування введених команд у файл JSON-логів.
    Якщо файл відсутній або пошкоджений — створює новий.
    """
    logs = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []

    log_entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "user": "Користувач",
        "message": text
    }
    logs.append(log_entry)

    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Antony ⚠️] Помилка запису логу: {e}")

def get_user_input() -> str:
    """
    Отримує текстове повідомлення від користувача через CLI.
    - Ігнорує порожні рядки.
    - Захищає від спаму (повторів менше ніж через 2 секунди).
    - Логує всі введення.
    """
    global _last_input_time, _last_user_input

    while True:
        try:
            user_input = input("[Ти]: ").strip()

            if not user_input:
                print("[Antony]: Твоє мовчання голосніше за слова, але напиши щось :)")
                continue

            now = time.time()
            if user_input == _last_user_input and now - _last_input_time < 2:
                print("[Antony]: Ти щойно це казав. Є щось нове?")
                continue

            _last_input_time = now
            _last_user_input = user_input

            log_user_input(user_input)
            return user_input

        except EOFError:
            print("\n[Antony]: Завершення введення. До зустрічі.")
            return "вийти"
        except KeyboardInterrupt:
            print("\n[Antony]: Сеанс завершено вручну.")
            return "вийти"
        except Exception as e:
            print(f"[Antony]: Виникла помилка при введенні: {e}")
            continue