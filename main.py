import os
from cryptography.fernet import Fernet
from core.logic import process_command
from memory.memory import Memory
from encryption.secure_store import SecureVault
from interface.tts_output import speak
from interface.text_input import get_user_input
from dotenv import load_dotenv

def main():
    print("[Antony] Ініціалізація модулів...")

    # Завантажуємо змінні середовища з .env
    load_dotenv()

    # Отримуємо ключ із середовища або генеруємо (рекомендується з .env)
    vault_key = os.getenv("VAULT_KEY")
    if not vault_key:
        vault_key = Fernet.generate_key().decode()
        print(f"[Antony] 🔐 Згенеровано новий ключ для VAULT_KEY:\n{vault_key}")
        print("[Antony] Додай цей ключ у свій .env файл у форматі:\nVAULT_KEY=тут_твій_ключ")

    # Ініціалізація зашифрованої памʼяті
    vault = SecureVault("data/vault.json", key=vault_key)
    memory = Memory(vault)

    # Початкове вітання
    speak("Привіт! Я Antony. Я готовий до роботи.")

    while True:
        try:
            user_input = get_user_input()

            if not user_input.strip():
                continue

            if user_input.lower() in ["вийти", "exit", "quit"]:
                speak("До зустрічі! Я завжди поруч.")
                break

            # Обробляємо команду і отримуємо відповідь
            response = process_command(user_input, memory)

            # Відповідаємо голосом
            speak(response)

        except KeyboardInterrupt:
            speak("Сеанс завершено вручну.")
            break
        except Exception as e:
            speak("Вибач, сталася помилка під час обробки.")
            print(f"[Antony ⚠️] Error: {e}")

if __name__ == "__main__":
    main()