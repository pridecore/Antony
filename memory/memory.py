import datetime
import hashlib


class Memory:
    def __init__(self, vault):
        """
        Ініціалізація памʼяті з переданим шифрованим сховищем.
        :param vault: SecureVault instance
        """
        self.vault = vault
        self.data = self.vault.load() or []

    def _hash_text(self, text: str) -> str:
        """Генерує хеш тексту (SHA-256) для унікальності."""
        return hashlib.sha256(text.encode()).hexdigest()

    def save(self, text: str):
        """
        Зберігає новий факт у памʼять Antony.
        :param text: Що запамʼятати
        """
        entry = {
            "id": self._hash_text(text + str(datetime.datetime.now())),
            "timestamp": datetime.datetime.now().isoformat(),
            "text": text.strip()
        }
        self.data.append(entry)
        self.vault.save(self.data)

    def recall(self, limit=3, show_timestamp=True):
        """
        Повертає останні збережені факти.
        :param limit: Скільки останніх спогадів вивести
        :param show_timestamp: Чи показувати час
        :return: Список рядків
        """
        recent = self.data[-limit:]
        if show_timestamp:
            return [f"{e['timestamp']}: {e['text']}" for e in recent]
        return [e["text"] for e in recent]

    def search(self, keyword: str):
        """
        Пошук у памʼяті за ключовим словом.
        :param keyword: слово або фраза
        :return: список збігів
        """
        return [e for e in self.data if keyword.lower() in e["text"].lower()]

    def forget(self, keyword: str) -> int:
        """
        Видаляє всі записи, що містять keyword.
        :param keyword: текст для видалення
        :return: кількість видалених
        """
        before = len(self.data)
        self.data = [e for e in self.data if keyword.lower() not in e["text"].lower()]
        self.vault.save(self.data)
        return before - len(self.data)