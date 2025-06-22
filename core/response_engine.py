import random

TEMPLATES = {
    "greeting": [
        "Привіт! Як ти сьогодні?",
        "Вітаю, друже! Радіймо дню!",
        "Привіт, я знову тут для тебе.",
        "Добрий день! Готовий допомогти."
    ],

    "farewell": [
        "До зустрічі! Гарного тобі дня.",
        "Бувай! Завжди поруч.",
        "Відпочивай, я залишаюсь на зв’язку.",
        "На все добре! Я завжди поруч."
    ],

    "gratitude": [
        "Дякую за твої слова!",
        "Це дуже приємно чути.",
        "Я вдячний тобі.",
        "Завжди радий допомогти."
    ],

    "recall_memory_empty": [
        "Я ще нічого не зберіг у своїй памʼяті.",
        "Моя памʼять наразі порожня.",
        "Наразі я нічого не памʼятаю зі збереженого."
    ],

    "recall_memory_filled": [
        "Я памʼятаю наступне:\n{facts}",
        "У моїй памʼяті є такі записи:\n{facts}",
        "Ось що я зберіг:\n{facts}"
    ],

    "current_time": [
        "Зараз {time}.",
        "На годиннику {time}.",
        "Точний час: {time}."
    ],

    "ethical_hacking": [
        "Ось що вдалося дізнатися:\n\n🔹 IP: {ip}\n🔹 Інтерфейси:\n{interfaces}\n🔹 Відкриті порти:\n{ports}",
        "Результати сканування:\n🌐 IP: {ip}\n🧩 Інтерфейси:\n{interfaces}\n📡 Портскан:\n{ports}"
    ],

    "security_audit": [
        "Системна інформація:\n{sys_info}\n\nАудит:\n{audit}",
        "🔐 Звіт безпеки:\n\n{sys_info}\n\nРезультат:\n{audit}"
    ],

    "unknown": [
        "Це трохи за межами мого розуміння. Поясни простіше?",
        "Ще не знаю, як на це відповісти, але намагаюсь навчитися.",
        "Можливо, переформулюй? Я поки вчуся."
    ]
}


def generate_response(intent: str, data: dict = None) -> str:
    """
    Генерує відповідь на основі наміру та контексту (опційно).
    :param intent: Назва наміру
    :param data: Дані для підстановки
    :return: Згенерована фраза
    """
    data = data or {}

    # Обробка памʼяті
    if intent == "recall_memory":
        facts = data.get("facts", [])
        if not facts:
            return random.choice(TEMPLATES["recall_memory_empty"])
        joined = "\n- " + "\n- ".join(facts)
        return random.choice(TEMPLATES["recall_memory_filled"]).format(facts=joined)

    # Інші інтенси з параметрами
    if intent in TEMPLATES:
        template = random.choice(TEMPLATES[intent])
        try:
            return template.format(**data)
        except KeyError as e:
            return f"[response_engine] ⚠️ Відсутній параметр у шаблоні: {str(e)}"

    # За замовчуванням
    return random.choice(TEMPLATES["unknown"])