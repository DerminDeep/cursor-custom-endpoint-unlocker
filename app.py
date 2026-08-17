import os
import sys
import io
import base64
import shutil
import subprocess
import webbrowser
import threading
from datetime import datetime
from PIL import Image
import customtkinter as ctk

# Ensure current working directory is script folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

APP_DIR = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser(r'~\AppData\Local')), 'Programs', 'cursor', 'resources', 'app')
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser(r'~\AppData\Roaming')), 'Cursor')
CURSOR_EXE = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser(r'~\AppData\Local')), 'Programs', 'cursor', 'Cursor.exe')

TARGET_FILES = [
    os.path.join(APP_DIR, 'out', 'main.js'),
    os.path.join(APP_DIR, 'out', 'vs', 'workbench', 'api', 'node', 'extensionHostProcess.js'),
    os.path.join(APP_DIR, 'out', 'vs', 'workbench', 'workbench.desktop.main.js'),
    os.path.join(APP_DIR, 'out', 'vs', 'workbench', 'workbench.glass.main.js')
]

CACHE_DIRS = [
    os.path.join(APPDATA_DIR, 'Code Cache'),
    os.path.join(APPDATA_DIR, 'CachedData'),
    os.path.join(APPDATA_DIR, 'GPUCache'),
    os.path.join(APPDATA_DIR, 'Service Worker', 'ScriptCache'),
    os.path.join(APPDATA_DIR, 'Partitions', 'cursor-browser', 'Code Cache'),
    os.path.join(APPDATA_DIR, 'DawnGraphiteCache'),
    os.path.join(APPDATA_DIR, 'DawnWebGPUCache')
]

# Theme Colors
ORANGE = "#FF7A00"
ORANGE_HOVER = "#FF9124"
ORANGE_SUBTLE = "#2A1805"
BG_BASE = "#0C0D11"
CARD_BG = "#14161D"
CARD_HOVER = "#1B1E28"
BORDER_SUBTLE = "#20232E"
TEXT_MAIN = "#FFFFFF"
TEXT_MUTED = "#7A8293"
GREEN = "#34C759"
RED = "#FF453A"

# 100% Official GitHub Octocat Silhouette (White #FFFFFF on Transparent)
OFFICIAL_OCTOCAT_WHITE_B64 = "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"

# Translations
LANG = {
    "English": {
        "title": "Cursor Unlocker",
        "subtitle": "Custom endpoint activator for Cursor IDE",
        "status_provider": "PROVIDER STATUS",
        "status_process": "CURSOR PROCESS",
        "status_version": "VERSION",
        "checking": "● CHECKING",
        "unlocked": "● UNLOCKED",
        "locked": "● LOCKED",
        "running": "● RUNNING",
        "stopped": "● STOPPED",
        "btn_unlock": "⚡  Unlock Local Provider",
        "btn_lock": "🔒  Restore / Lock",
        "btn_cache": "🧹  Purge V8 Cache",
        "btn_kill": "🛑  Kill Cursor",
        "btn_launch": "🚀  Launch Cursor",
        "log_title": "ACTIVITY LOG",
        "log_clear": "clear",
        "log_init": "Ready. Language: English.",
        "log_unlock_start": "Unlocking Local Provider...",
        "log_unlock_ok": "Success! Unlocked {count} files. V8 cache purged.",
        "log_lock_start": "Restoring default state...",
        "log_lock_ok": "Restored default in {count} files. V8 cache purged.",
        "log_kill": "Cursor processes terminated.",
        "log_cache": "Cleared {count} cache folders.",
        "log_launch": "Launching Cursor IDE...",
        "log_not_found": "Cursor.exe not found.",
        "github_author": "  DerminDeep"
    },
    "Русский": {
        "title": "Cursor Unlocker",
        "subtitle": "Активатор кастомных эндпоинтов для Cursor IDE",
        "status_provider": "СТАТУС ПРОВАЙДЕРА",
        "status_process": "ПРОЦЕСС CURSOR",
        "status_version": "ВЕРСИЯ",
        "checking": "● ПРОВЕРКА",
        "unlocked": "● РАЗБЛОКИРОВАНО",
        "locked": "● ЗАБЛОКИРОВАНО",
        "running": "● ЗАПУЩЕН",
        "stopped": "● ОСТАНОВЛЕН",
        "btn_unlock": "⚡  Разблокировать Local Provider",
        "btn_lock": "🔒  Восстановить (Lock)",
        "btn_cache": "🧹  Очистить V8 Кэш",
        "btn_kill": "🛑  Закрыть Cursor",
        "btn_launch": "🚀  Запустить Cursor",
        "log_title": "ЖУРНАЛ ДЕЙСТВИЙ",
        "log_clear": "очистить",
        "log_init": "Готово. Язык: Русский.",
        "log_unlock_start": "Разблокировка Local Provider...",
        "log_unlock_ok": "Успешно! Разблокировано {count} файлов. V8 кэш очищен.",
        "log_lock_start": "Восстановление исходного состояния...",
        "log_lock_ok": "Исходное состояние возвращено ({count} файлов).",
        "log_kill": "Процессы Cursor закрыты.",
        "log_cache": "Очищено {count} папок кэша V8/GPU.",
        "log_launch": "Запуск Cursor IDE...",
        "log_not_found": "Cursor.exe не найден.",
        "github_author": "  DerminDeep"
    }
}

class MinimalUnlockerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "English"
        self.title("Cursor Local Unlocker — DerminDeep")
        self.geometry("650x600")
        self.minsize(600, 560)
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        self.configure(fg_color=BG_BASE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Load Pure White Official Octocat Icon
        self.gh_icon = self.load_octocat_white_icon(18)

        self.init_ui()
        self.log(self.t("log_init"))
        self.update_status()
        self.poll_status()

    def t(self, key):
        return LANG[self.current_lang].get(key, key)

    def load_octocat_white_icon(self, size=18):
        try:
            raw_bytes = base64.b64decode(OFFICIAL_OCTOCAT_WHITE_B64)
            pil_img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
            return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(size, size))
        except Exception:
            return None

    def init_ui(self):
        # 1. HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=24, pady=(20, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")

        title_row = ctk.CTkFrame(title_box, fg_color="transparent")
        title_row.pack(anchor="w")

        self.lbl_title = ctk.CTkLabel(title_row, text=self.t("title"), font=("Segoe UI", 18, "bold"), text_color=TEXT_MAIN)
        self.lbl_title.pack(side="left")

        ctk.CTkLabel(
            title_row, text="LOCAL", font=("Segoe UI", 10, "bold"),
            fg_color=ORANGE_SUBTLE, text_color=ORANGE,
            corner_radius=4, padx=6, pady=2
        ).pack(side="left", padx=8)

        self.lbl_subtitle = ctk.CTkLabel(title_box, text=self.t("subtitle"), font=("Segoe UI", 12), text_color=TEXT_MUTED)
        self.lbl_subtitle.pack(anchor="w", pady=(2, 0))

        # Right Controls (Language Segmented Switch + GitHub Button)
        right_box = ctk.CTkFrame(header, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e")

        # Explicit Language Dropdown / Segmented Selection
        self.lang_picker = ctk.CTkSegmentedButton(
            right_box, values=["English", "Русский"],
            font=("Segoe UI", 11, "bold"),
            fg_color=CARD_BG, selected_color=ORANGE, selected_hover_color=ORANGE_HOVER,
            unselected_color=CARD_BG, unselected_hover_color=CARD_HOVER,
            text_color="#FFFFFF",
            corner_radius=18, height=34, width=150,
            command=self.on_language_change
        )
        self.lang_picker.set("English")
        self.lang_picker.pack(side="left", padx=(0, 10))

        # GitHub Button with Pure White Official Icon
        if self.gh_icon:
            self.btn_gh = ctk.CTkButton(
                right_box, text=self.t("github_author"), image=self.gh_icon, compound="left",
                font=("Segoe UI", 12, "bold"), fg_color=CARD_BG, hover_color=CARD_HOVER,
                text_color="#FFFFFF", border_width=1, border_color=BORDER_SUBTLE,
                corner_radius=18, height=36,
                command=self.open_github
            )
        else:
            self.btn_gh = ctk.CTkButton(
                right_box, text="DerminDeep",
                font=("Segoe UI", 12, "bold"), fg_color=CARD_BG, hover_color=CARD_HOVER,
                text_color="#FFFFFF", border_width=1, border_color=BORDER_SUBTLE,
                corner_radius=18, height=36,
                command=self.open_github
            )
        self.btn_gh.pack(side="left")

        # 2. STATUS STRIP
        status_bar = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_SUBTLE)
        status_bar.grid(row=1, column=0, padx=24, pady=(0, 14), sticky="ew")
        status_bar.grid_columnconfigure((0, 1, 2), weight=1)

        f1 = ctk.CTkFrame(status_bar, fg_color="transparent")
        f1.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        self.hdr_provider = ctk.CTkLabel(f1, text=self.t("status_provider"), font=("Segoe UI", 9, "bold"), text_color=TEXT_MUTED)
        self.hdr_provider.pack(anchor="w")
        self.lbl_provider = ctk.CTkLabel(f1, text=self.t("checking"), font=("Segoe UI", 12, "bold"), text_color=ORANGE)
        self.lbl_provider.pack(anchor="w")

        f2 = ctk.CTkFrame(status_bar, fg_color="transparent")
        f2.grid(row=0, column=1, padx=16, pady=10, sticky="w")
        self.hdr_process = ctk.CTkLabel(f2, text=self.t("status_process"), font=("Segoe UI", 9, "bold"), text_color=TEXT_MUTED)
        self.hdr_process.pack(anchor="w")
        self.lbl_process = ctk.CTkLabel(f2, text=self.t("stopped"), font=("Segoe UI", 12, "bold"), text_color=TEXT_MUTED)
        self.lbl_process.pack(anchor="w")

        f3 = ctk.CTkFrame(status_bar, fg_color="transparent")
        f3.grid(row=0, column=2, padx=16, pady=10, sticky="w")
        self.hdr_version = ctk.CTkLabel(f3, text=self.t("status_version"), font=("Segoe UI", 9, "bold"), text_color=TEXT_MUTED)
        self.hdr_version.pack(anchor="w")
        ctk.CTkLabel(f3, text="● 3.16.17", font=("Segoe UI", 12, "bold"), text_color=TEXT_MAIN).pack(anchor="w")

        # 3. ACTIONS PANEL
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, padx=24, pady=0, sticky="ew")
        actions.grid_columnconfigure((0, 1), weight=1)

        self.btn_unlock = ctk.CTkButton(
            actions, text=self.t("btn_unlock"),
            font=("Segoe UI", 14, "bold"),
            fg_color=ORANGE, hover_color=ORANGE_HOVER,
            text_color="#000000", corner_radius=10, height=44,
            command=self.action_unlock
        )
        self.btn_unlock.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="ew")

        self.btn_lock = ctk.CTkButton(
            actions, text=self.t("btn_lock"), font=("Segoe UI", 12, "bold"),
            fg_color=CARD_BG, hover_color=CARD_HOVER, text_color=TEXT_MAIN,
            border_width=1, border_color=BORDER_SUBTLE, corner_radius=8, height=36,
            command=self.action_lock
        )
        self.btn_lock.grid(row=1, column=0, padx=(0, 4), pady=4, sticky="ew")

        self.btn_cache = ctk.CTkButton(
            actions, text=self.t("btn_cache"), font=("Segoe UI", 12, "bold"),
            fg_color=CARD_BG, hover_color=CARD_HOVER, text_color=TEXT_MAIN,
            border_width=1, border_color=BORDER_SUBTLE, corner_radius=8, height=36,
            command=self.action_clear_cache
        )
        self.btn_cache.grid(row=1, column=1, padx=(4, 0), pady=4, sticky="ew")

        self.btn_kill = ctk.CTkButton(
            actions, text=self.t("btn_kill"), font=("Segoe UI", 12, "bold"),
            fg_color=CARD_BG, hover_color="#2B1414", text_color=RED,
            border_width=1, border_color=BORDER_SUBTLE, corner_radius=8, height=36,
            command=self.action_kill
        )
        self.btn_kill.grid(row=2, column=0, padx=(0, 4), pady=4, sticky="ew")

        self.btn_launch = ctk.CTkButton(
            actions, text=self.t("btn_launch"), font=("Segoe UI", 12, "bold"),
            fg_color=CARD_BG, hover_color="#12261A", text_color=GREEN,
            border_width=1, border_color=BORDER_SUBTLE, corner_radius=8, height=36,
            command=self.action_launch
        )
        self.btn_launch.grid(row=2, column=1, padx=(4, 0), pady=4, sticky="ew")

        # 4. LOG CONSOLE
        log_box = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_SUBTLE)
        log_box.grid(row=3, column=0, padx=24, pady=(12, 16), sticky="nsew")
        log_box.grid_columnconfigure(0, weight=1)
        log_row = 1
        log_box.grid_rowconfigure(log_row, weight=1)

        log_head = ctk.CTkFrame(log_box, fg_color="transparent")
        log_head.grid(row=0, column=0, padx=12, pady=(8, 4), sticky="ew")
        log_head.grid_columnconfigure(0, weight=1)

        self.hdr_log = ctk.CTkLabel(log_head, text=self.t("log_title"), font=("Consolas", 10, "bold"), text_color=TEXT_MUTED)
        self.hdr_log.grid(row=0, column=0, sticky="w")

        self.btn_clear = ctk.CTkButton(
            log_head, text=self.t("log_clear"), width=44, height=20, font=("Segoe UI", 10),
            fg_color="transparent", hover_color=BORDER_SUBTLE, text_color=TEXT_MUTED,
            command=self.clear_logs
        )
        self.btn_clear.grid(row=0, column=1, sticky="e")

        self.txt_log = ctk.CTkTextbox(
            log_box, fg_color="#0A0B0E", text_color=ORANGE_HOVER,
            font=("Consolas", 11), activate_scrollbars=True, corner_radius=6
        )
        self.txt_log.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.txt_log.configure(state="disabled")

    def on_language_change(self, value):
        self.current_lang = value
        self.lbl_title.configure(text=self.t("title"))
        self.lbl_subtitle.configure(text=self.t("subtitle"))
        self.hdr_provider.configure(text=self.t("status_provider"))
        self.hdr_process.configure(text=self.t("status_process"))
        self.hdr_version.configure(text=self.t("status_version"))
        self.btn_unlock.configure(text=self.t("btn_unlock"))
        self.btn_lock.configure(text=self.t("btn_lock"))
        self.btn_cache.configure(text=self.t("btn_cache"))
        self.btn_kill.configure(text=self.t("btn_kill"))
        self.btn_launch.configure(text=self.t("btn_launch"))
        self.hdr_log.configure(text=self.t("log_title"))
        self.btn_clear.configure(text=self.t("log_clear"))
        self.update_status()
        self.log(self.t("log_init"))

    def log(self, text):
        now = datetime.now().strftime("%H:%M:%S")
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"[{now}] {text}\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def clear_logs(self):
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")

    def update_status(self):
        unlocked = 0
        total = len(TARGET_FILES)

        for f in TARGET_FILES:
            if os.path.exists(f):
                try:
                    with open(f, 'r', encoding='latin1') as fp:
                        if 'localMode:!0' in fp.read():
                            unlocked += 1
                except Exception:
                    pass

        if unlocked == total and total > 0:
            self.lbl_provider.configure(text=f"{self.t('unlocked')} ({unlocked}/{total})", text_color=GREEN)
        else:
            self.lbl_provider.configure(text=f"{self.t('locked')} ({unlocked}/{total})", text_color=RED)

        is_running = False
        try:
            out = subprocess.check_output('tasklist /FI "IMAGENAME eq Cursor.exe" /NH', shell=True, text=True, stderr=subprocess.DEVNULL)
            is_running = 'cursor.exe' in out.lower()
        except Exception:
            pass

        if is_running:
            self.lbl_process.configure(text=self.t("running"), text_color=GREEN)
        else:
            self.lbl_process.configure(text=self.t("stopped"), text_color=TEXT_MUTED)

    def poll_status(self):
        self.update_status()
        self.after(3500, self.poll_status)

    def action_kill(self):
        try:
            subprocess.run("taskkill /F /IM Cursor.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.log(self.t("log_kill"))
        except Exception:
            pass
        self.update_status()

    def action_clear_cache(self):
        cleared = 0
        for d in CACHE_DIRS:
            if os.path.exists(d):
                try:
                    shutil.rmtree(d, ignore_errors=True)
                    cleared += 1
                except Exception:
                    pass
        self.log(self.t("log_cache").format(count=cleared))

    def action_unlock(self):
        threading.Thread(target=self._unlock_worker, daemon=True).start()

    def _unlock_worker(self):
        self.log(self.t("log_unlock_start"))
        self.action_kill()

        modified = 0
        for f in TARGET_FILES:
            if not os.path.exists(f):
                continue
            try:
                with open(f, 'r', encoding='latin1') as fp:
                    content = fp.read()

                if 'localMode:!1' in content:
                    content = content.replace('localMode:!1', 'localMode:!0')
                    with open(f, 'w', encoding='latin1') as fp:
                        fp.write(content)
                    modified += 1
            except Exception:
                pass

        self.action_clear_cache()
        self.log(self.t("log_unlock_ok").format(count=modified))
        self.update_status()

    def action_lock(self):
        threading.Thread(target=self._lock_worker, daemon=True).start()

    def _lock_worker(self):
        self.log(self.t("log_lock_start"))
        self.action_kill()

        modified = 0
        for f in TARGET_FILES:
            if not os.path.exists(f):
                continue
            try:
                with open(f, 'r', encoding='latin1') as fp:
                    content = fp.read()

                if 'localMode:!0' in content:
                    content = content.replace('localMode:!0', 'localMode:!1')
                    with open(f, 'w', encoding='latin1') as fp:
                        fp.write(content)
                    modified += 1
            except Exception:
                pass

        self.action_clear_cache()
        self.log(self.t("log_lock_ok").format(count=modified))
        self.update_status()

    def action_launch(self):
        if os.path.exists(CURSOR_EXE):
            self.log(self.t("log_launch"))
            subprocess.Popen([CURSOR_EXE], shell=True)
            self.after(1500, self.update_status)
        else:
            self.log(self.t("log_not_found"))

    def open_github(self):
        webbrowser.open_new_tab("https://github.com/DerminDeep")

if __name__ == "__main__":
    app = MinimalUnlockerApp()
    app.mainloop()
