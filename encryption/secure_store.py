import json
import os
from cryptography.fernet import Fernet

class SecureVault:
    def __init__(self, filepath: str, key: str = None):
        """
        Клас для безпечного зберігання та читання зашифрованих даних у JSON-файлі.
        
        :param filepath: шлях до зашифрованого JSON-файлу
        :param key: ключ шифрування (base64 рядок); якщо None — береться з .env
        """
        self.filepath = filepath
        self.key = key or os.getenv("VAULT_KEY")

        if not self.key:
            raise ValueError("🔐 Ключ шифрування не знайдено. Встанови VAULT_KEY у .env")

        # Переконуємося, що ключ у форматі байтів
        if isinstance(self.key, str):
            self.key = self.key.encode()

        self.fernet = Fernet(self.key)

    def save(self, data):
        """
        Шифрує і зберігає дані у файл.
        
        :param data: Python-обʼєкт, що буде конвертований у JSON і зашифрований
        """
        try:
            raw = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
            encrypted = self.fernet.encrypt(raw)
            with open(self.filepath, "wb") as f:
                f.write(encrypted)
        except Exception as e:
            print(f"[SecureVault] Помилка при збереженні: {e}")

    def load(self):
        """
        Завантажує і розшифровує дані з файлу.
        
        :return: Python-обʼєкт (список, словник тощо), або пустий список, якщо файл відсутній чи пошкоджений
        """
        if not os.path.exists(self.filepath):
            # Якщо файлу немає, повертаємо порожній список (памʼять пуста)
            return []

        try:
            with open(self.filepath, "rb") as f:
                encrypted = f.read()
            if not encrypted:
                # Порожній файл, повертаємо порожній список
                return []
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            print(f"[SecureVault] Помилка при зчитуванні: {e}")
            # У випадку помилки — не падаємо, а повертаємо пустий список
            return []