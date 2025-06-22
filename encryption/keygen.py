from cryptography.fernet import Fernet
import os

ENV_PATH = ".env"
KEY_NAME = "VAULT_KEY"

def generate_key():
    key = Fernet.generate_key().decode()

    # Якщо .env вже існує — перевірити, чи є ключ
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            lines = f.readlines()
        if any(line.startswith(KEY_NAME) for line in lines):
            print(f"[keygen] ⚠️  {KEY_NAME} вже існує в .env. Новий ключ НЕ записано.")
            print(f"[keygen] Поточний ключ: {get_current_key(lines)}")
            return

    # Додаємо ключ
    with open(ENV_PATH, "a") as f:
        f.write(f"{KEY_NAME}={key}\n")

    print(f"[keygen] ✅ Ключ успішно згенеровано і записано у .env:")
    print(f"[keygen] {KEY_NAME}={key}")

def get_current_key(lines):
    for line in lines:
        if line.startswith(KEY_NAME):
            return line.strip().split("=")[1]
    return None

if __name__ == "__main__":
    generate_key()