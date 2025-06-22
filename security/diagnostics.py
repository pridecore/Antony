import subprocess
import platform
import socket
import os

def get_open_ports(host="127.0.0.1"):
    try:
        result = subprocess.check_output(["nmap", "-p-", host], stderr=subprocess.DEVNULL)
        return result.decode("utf-8")
    except FileNotFoundError:
        return "[diagnostics] ❌ Nmap не встановлено. Встановіть nmap для сканування портів."
    except Exception as e:
        return f"[diagnostics] ❌ Помилка при скануванні портів: {str(e)}"

def get_network_interfaces():
    try:
        command = ["ifconfig"] if platform.system() != "Windows" else ["ipconfig"]
        result = subprocess.check_output(command, stderr=subprocess.DEVNULL)
        return result.decode("utf-8")
    except Exception as e:
        return f"[diagnostics] ❌ Помилка при отриманні мережевих інтерфейсів: {str(e)}"

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return f"[diagnostics] 🧭 Локальна IP-адреса: {local_ip}"
    except Exception as e:
        return f"[diagnostics] ❌ Не вдалося визначити IP: {str(e)}"

def get_system_info():
    return (
        f"[diagnostics] 🖥️ Система: {platform.system()}\n"
        f"[diagnostics] Версія: {platform.version()}\n"
        f"[diagnostics] Процесор: {platform.processor()}"
    )

def get_firewall_status():
    try:
        if platform.system() == "Darwin":
            result = subprocess.check_output(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"])
        elif platform.system() == "Linux":
            result = subprocess.check_output(["ufw", "status"])
        else:
            return "[diagnostics] 🔥 Перевірка firewall не підтримується на цій ОС."
        return f"[diagnostics] 🔥 Firewall статус:\n{result.decode('utf-8')}"
    except Exception as e:
        return f"[diagnostics] ❌ Не вдалося перевірити firewall: {str(e)}"

def check_rootkits():
    try:
        result = subprocess.check_output(["chkrootkit"], stderr=subprocess.DEVNULL)
        return f"[diagnostics] 🦠 Rootkit перевірка:\n{result.decode('utf-8')}"
    except FileNotFoundError:
        return "[diagnostics] 🦠 chkrootkit не встановлено. Пропускаю перевірку rootkit."
    except Exception as e:
        return f"[diagnostics] ❌ Помилка rootkit перевірки: {str(e)}"

def get_active_connections():
    try:
        result = subprocess.check_output(["netstat", "-tunap"], stderr=subprocess.DEVNULL)
        return f"[diagnostics] 🔌 Активні підключення:\n{result.decode('utf-8')}"
    except Exception as e:
        return f"[diagnostics] ❌ Не вдалося отримати з’єднання: {str(e)}"

def ping_test(host="8.8.8.8"):
    try:
        result = subprocess.check_output(["ping", "-c", "4", host], stderr=subprocess.DEVNULL)
        return f"[diagnostics] 📶 Ping результат:\n{result.decode('utf-8')}"
    except Exception as e:
        return f"[diagnostics] ❌ Помилка ping: {str(e)}"

def traceroute(host="8.8.8.8"):
    try:
        result = subprocess.check_output(["traceroute", host], stderr=subprocess.DEVNULL)
        return f"[diagnostics] 🛰️ Traceroute:\n{result.decode('utf-8')}"
    except Exception as e:
        return f"[diagnostics] ❌ Помилка traceroute: {str(e)}"

def read_system_logs():
    logs = []
    possible_paths = ["/var/log/system.log", "/var/log/syslog", "/var/log/auth.log"]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    content = f.read()[-1500:]  # останні ~1500 символів
                    logs.append(f"[diagnostics] 📂 Лог {path}:\n{content}")
            except Exception as e:
                logs.append(f"[diagnostics] ❌ Не вдалося прочитати {path}: {str(e)}")
    return "\n\n".join(logs) if logs else "[diagnostics] ℹ️ Логи не знайдено або не доступні."

def run_security_audit():
    return "\n".join([
        get_system_info(),
        get_local_ip(),
        get_firewall_status(),
        get_open_ports(),
        get_active_connections(),
        check_rootkits(),
        read_system_logs(),
        ping_test(),
        traceroute()
    ])