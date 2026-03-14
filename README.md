# RAT System Contol Bot in Telegram
only for windows
***
### Commands
* **``/help`` - all commands**
* **``/scr`` - takes a screenshot of the entire screen**
* **``/run`` - runs command from cmd**
* **``/write`` - entrys any text**
* **``/key`` - presses any keys, for example: `f12` or `shift`**
* **``/ct_notify`` - dialog window based on `ctypes`**
* **``/pl_notify`` - notification based on `plyer`**
* **``/sinfo`` - all information about system**
* **``/pinfo`` - information about all active windows**
* **``/clipb`` - getting any text from clipboard**
* **``/web`` - opening any urls**
* **``/moff`` - disabling monitor**
* **``/mon`` - enabling monitor**
* **``/mlock`` - blocking monitor (`Win+L`)**
* **``/wkill`` - killing active window**
* **``/shutdown`` - have 2 arg: `r (reboot)` and `s (shutdown)`. this command can shutdown and reboot your pc**
* **``/pscan`` - scanning all ports in `local ip`**
* **``/bsod`` - calling BLue Screen Of Death / [BSOD ](https://i.ytimg.com/vi/Rom6IUmQj-4/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH2CIAC0AWKAgwIABABGBMgTih_MA8=&amp;rs=AOn4CLDyJNckGfEAcydWc5y7qjuU_ygd5A)**
***
### Usage
1. **Set your `_TOKEN_` and `_ADMIN_ID_` in the script**
2. **Install requests. move to the location where the located ``requirements.txt`` and install pip from this list:**
   ```
   pip install -r requirements.txt
   ```
3. **Run the bot:**
   ```shell
   python RemoteBot.py
   ```
4. **Use commands in Telegram to control your system**

***
### Security
* **Only the ``_ADMIN_ID_`` can execute commands**
* **Keep your ``TOKEN`` private**
* **Bot will notify you if another user tries to press ``/start`` command**


