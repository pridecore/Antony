import sys
import platform
from datetime import datetime

def _timestamp() -> str:
    """Поточний час у форматі [HH:MM:SS]."""
    return datetime.now().strftime("[%H:%M:%S]")

def notify_info(message: str):
    """
    Виводить інформаційне повідомлення з часовою позначкою.
    """
    print(f"{_timestamp()} [INFO] {message}")

def notify_warning(message: str):
    """
    Виводить повідомлення-попередження з часовою позначкою.
    """
    print(f"{_timestamp()} [WARNING] {message}")

def notify_error(message: str):
    """
    Виводить повідомлення про помилку з часовою позначкою.
    """
    print(f"{_timestamp()} [ERROR] {message}")

def beep():
    """
    Відтворює звуковий сигнал у консолі.
    Підтримує Windows (winsound) та Unix-подібні системи (ASCII bell).
    """
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 200)  # Частота 1000 Гц, тривалість 200 мс
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()
    except Exception as e:
        notify_error(f"Не вдалося відтворити звуковий сигнал: {e}")

def notify_with_beep(message: str):
    """
    Відтворює звуковий сигнал і виводить інформаційне повідомлення.
    """
    beep()
    notify_info(message)

# Приклад використання (можна закоментувати або прибрати)
if __name__ == "__main__":
    notify_info("Система Antony запущена.")
    notify_warning("Це тестове попередження.")
    notify_error("Це тестова помилка.")
    notify_with_beep("Нове повідомлення з сигналом!")