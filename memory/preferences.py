import json
import os

class Preferences:
    def __init__(self, path="data/preferences.json"):
        """
        Ініціалізує обʼєкт користувацьких налаштувань.
        :param path: шлях до JSON-файлу з вподобаннями
        """
        self.path = path
        self.defaults = {
            "name": "Користувач",
            "language": "uk",
            "voice": "default",
            "mode": "normal",  # або "developer"
            "response_style": "detailed",  # або "concise"
            "wake_word": "antony",
            "auto_listen": False
        }
        self.data = self._load()

    def _load(self):
        """Завантажує вподобання з файлу або створює стандартні."""
        if not os.path.exists(self.path):
            self._save(self.defaults)
            return self.defaults.copy()
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                prefs = json.load(f)
                # автооновлення нових ключів
                for key in self.defaults:
                    prefs.setdefault(key, self.defaults[key])
                return prefs
        except Exception:
            return self.defaults.copy()

    def _save(self, prefs):
        """Зберігає вподобання до JSON."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=4, ensure_ascii=False)

    def get(self, key):
        """Отримати значення за ключем."""
        return self.data.get(key, self.defaults.get(key))

    def set(self, key, value):
        """Оновити значення і зберегти."""
        self.data[key] = value
        self._save(self.data)

    def reset(self):
        """Скинути всі вподобання до дефолтних."""
        self.data = self.defaults.copy()
        self._save(self.data)

    def all(self):
        """Отримати всі налаштування."""
        return self.data.copy()

    def __str__(self):
        """Стильне виведення вподобань."""
        return "\n".join([f"🔧 {k}: {v}" for k, v in self.data.items()])