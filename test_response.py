from core.response_engine import generate_response
from core.logic import process_command
from memory.memory import Memory
from encryption.secure_store import SecureVault
from cryptography.fernet import Fernet
import os

def test_secure_vault():
    print("\n--- Тест SecureVault ---")

    key = Fernet.generate_key().decode()
    test_file = "data/test_vault.json"

    # Видаляємо, якщо існує
    if os.path.exists(test_file):
        os.remove(test_file)

    vault = SecureVault(test_file, key=key)
    test_data = [
        {"timestamp": "2025-06-22T10:00:00", "text": "Перша запис"},
        {"timestamp": "2025-06-22T11:00:00", "text": "Друга запис"}
    ]

    vault.save(test_data)
    print("Дані збережено.")

    loaded_data = vault.load()
    print("Дані завантажено:", loaded_data)

    assert loaded_data == test_data, "Помилка: дані після збереження і завантаження не співпадають!"

    # Чистимо після тесту
    if os.path.exists(test_file):
        os.remove(test_file)

    print("Тест SecureVault пройдено успішно.")

def test_response_engine():
    print("\n--- Тест response_engine ---")

    print("Greeting:", generate_response("greeting"))
    print("Farewell:", generate_response("farewell"))
    print("Gratitude:", generate_response("gratitude"))
    print("Unknown:", generate_response("unknown"))

    print("\nRecall memory (порожня):")
    print(generate_response("recall_memory", {"facts": []}))

    facts = ["Памʼятаю тебе", "Ти любиш програмувати", "Мені подобається допомагати"]
    print("\nRecall memory (з фактами):")
    print(generate_response("recall_memory", {"facts": facts}))

    print("\nCurrent time:")
    print(generate_response("current_time", {"time": "12:34:56"}))

    print("\nEthical hacking (скорочено):")
    print(generate_response("ethical_hacking", {
        "ip": "192.168.1.10",
        "interfaces": "eth0, wlan0",
        "ports": "22, 80, 443"
    }))

def test_logic_and_memory():
    print("\n--- Тест logic.py та memory.py ---")

    test_key = Fernet.generate_key().decode()
    vault = SecureVault("data/vault.json", key=test_key)
    memory = Memory(vault)

    print(process_command("запамʼятай що Python — це круто", memory))
    print(process_command("запамʼятай, що люблю чай", memory))
    print(process_command("що я тобі казав?", memory))
    print(process_command("привіт", memory))
    print(process_command("який зараз час?", memory))
    print(process_command("Що таке чорні діри?", memory))

if __name__ == "__main__":
    test_secure_vault()
    test_response_engine()
    test_logic_and_memory()