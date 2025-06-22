from datetime import datetime
import pytz  # Імпорт pytz для роботи з часовими зонами
from core.intents import detect_intent
from core.response_engine import generate_response
from core.affect import update_emotional_state, get_emotional_prefix
from security.diagnostics import (
    get_open_ports,
    get_network_interfaces,
    get_local_ip,
    get_system_info,
    run_security_audit,
)


def process_command(user_input: str, memory) -> str:
    """
    Основна логіка обробки команд.
    Інтерпретує наміри, звертається до памʼяті, емоцій, інструментів і формує відповідь.
    """

    # Аналізуємо емоції користувача за фразою
    update_emotional_state(user_input)
    emotion_prefix = get_emotional_prefix()

    # Розпізнаємо інтенцію (наміри)
    intent = detect_intent(user_input.lower())

    # Отримуємо київський час через pytz
    kyiv_tz = pytz.timezone("Europe/Kyiv")
    now = datetime.now(kyiv_tz).strftime("%H:%M:%S")

    if intent == "greeting":
        return emotion_prefix + generate_response("greeting")

    elif intent == "farewell":
        return emotion_prefix + generate_response("farewell")

    elif intent == "gratitude":
        return emotion_prefix + generate_response("gratitude")

    elif intent == "recall_memory":
        facts = memory.recall()
        return emotion_prefix + generate_response("recall_memory", {"facts": facts})

    elif intent == "remember":
        memory.save(user_input)
        return emotion_prefix + "Я це запамʼятав."

    elif intent == "current_time":
        return emotion_prefix + generate_response("current_time", {"time": now})

    elif intent == "ethical_hacking":
        ports = get_open_ports()
        interfaces = get_network_interfaces()
        ip = get_local_ip()
        return emotion_prefix + generate_response("ethical_hacking", {
            "ports": ports,
            "interfaces": interfaces,
            "ip": ip
        })

    elif intent == "security_audit":
        sys_info = get_system_info()
        audit_report = run_security_audit()
        return emotion_prefix + generate_response("security_audit", {
            "sys_info": sys_info,
            "audit": audit_report
        })

    # Інші/невідомі запити
    return emotion_prefix + generate_response("unknown")