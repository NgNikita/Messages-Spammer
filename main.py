import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pyperclip
from pynput import keyboard

import config
from spammer import SpammerCore
from watchdog import SystemWatchdog


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.cfg = config.load_settings()

        ctk.set_appearance_mode(self.cfg.get('theme', 'dark'))
        ctk.set_default_color_theme("blue")

        self.title("(M-S) Messages Spammer")
        self.geometry("520x680")
        self.resizable(False, False)
        self.attributes("-topmost", self.cfg.get('always_on_top', '0') == '1')

        self.hotkey_listener = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._pid_file = os.path.join(base_dir, "app.pid")
        try:
            with open(self._pid_file, 'w') as f:
                f.write(str(os.getpid()))
        except Exception:
            pass

        self.core = SpammerCore(self.update_counter_ui, self.spam_finished_ui, self.update_status_ui)

        required_files = [
            os.path.join(base_dir, "spammer.py"),
            os.path.join(base_dir, "config.py"),
            os.path.join(base_dir, "Emergency Stop.bat"),
        ]
        self.watchdog = SystemWatchdog(required_files, heartbeat_check_func=True)
        self.watchdog.start()

        self.init_ui()
        self.hook_keys()
        self.start_heartbeat_loop()

    def start_heartbeat_loop(self):
        if hasattr(self, 'watchdog'):
            self.watchdog.ping_heartbeat()
        self.after(1000, self.start_heartbeat_loop)

    def init_ui(self):
        lang = self.cfg.get('lang', 'en')
        t = config.TEXTS[lang]

        # --- top ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(15, 0))

        self.btn_lang = ctk.CTkButton(self.top_frame, text="RU" if lang == "en" else "EN", width=60, command=self.toggle_lang)
        self.btn_lang.pack(side="left")

        self.btn_theme = ctk.CTkButton(self.top_frame, text="🌙" if self.cfg.get('theme', 'dark') == "light" else "☀️", width=60, command=self.toggle_theme)
        self.btn_theme.pack(side="left", padx=10)

        # --- spam text ---
        self.lbl_spam = ctk.CTkLabel(self, text=t['spam_lbl'])
        self.lbl_spam.pack(anchor="w", padx=20, pady=(10, 0))

        self.f_entry = ctk.CTkFrame(self, fg_color="transparent")
        self.f_entry.pack(fill="x", padx=20, pady=5)

        self.txt_entry = ctk.CTkTextbox(self.f_entry, height=90)
        self.txt_entry.pack(side="left", fill="x", expand=True)
        if self.cfg.get('spam_text'):
            self.txt_entry.insert("1.0", self.cfg.get('spam_text', ''))

        self.btn_paste = ctk.CTkButton(self.f_entry, text=t['paste'], width=70, command=self.paste_text)
        self.btn_paste.pack(side="right", padx=(5, 0), anchor="n")

        # --- delay ---
        self.lbl_delay = ctk.CTkLabel(self, text=t['delay_lbl'])
        self.lbl_delay.pack(anchor="w", padx=20, pady=(5, 0))
        self.delay_entry = ctk.CTkEntry(self)
        self.delay_entry.insert(0, self.cfg.get('delay', '1000'))
        self.delay_entry.pack(fill="x", padx=20, pady=2)

        # --- limit ---
        self.lbl_limit = ctk.CTkLabel(self, text=t['limit_lbl'])
        self.lbl_limit.pack(anchor="w", padx=20, pady=(5, 0))
        self.limit_entry = ctk.CTkEntry(self)
        self.limit_entry.insert(0, self.cfg.get('limit', '0'))
        self.limit_entry.pack(fill="x", padx=20, pady=2)

        # --- start / stop ---
        self.f_control = ctk.CTkFrame(self, fg_color="transparent")
        self.f_control.pack(pady=10)
        self.btn_start = ctk.CTkButton(
            self.f_control,
            text=t['start'].format(self.cfg.get('start_key', 'f1').upper()),
            fg_color="#28a745", hover_color="#218838",
            command=self.action_start,
        )
        self.btn_start.pack(side="left", padx=10)
        self.btn_stop = ctk.CTkButton(
            self.f_control,
            text=t['stop'].format(self.cfg.get('stop_key', 'f2').upper()),
            fg_color="#dc3545", hover_color="#c82333",
            state="disabled", command=self.action_stop,
        )
        self.btn_stop.pack(side="left", padx=10)

        # --- settings ---
        self.f_sett = ctk.CTkFrame(self)
        self.f_sett.pack(fill="x", padx=20, pady=5, ipady=3)

        self.lbl_sett_title = ctk.CTkLabel(self.f_sett, text=t['sett_title'], font=("Arial", 12, "bold"))
        self.lbl_sett_title.pack(anchor="w", padx=10, pady=2)

        self.f_sett_inner = ctk.CTkFrame(self.f_sett, fg_color="transparent")
        self.f_sett_inner.pack(fill="x", padx=10, pady=2)

        self.switch_smooth = ctk.CTkSwitch(self.f_sett_inner, text=t['sett_smooth'], command=self.toggle_smooth_cfg)
        self.switch_smooth.pack(side="left", padx=5)
        if self.cfg.get('smooth_theme', '1') == '1':
            self.switch_smooth.select()

        self.switch_ontop = ctk.CTkSwitch(self.f_sett_inner, text=t['sett_ontop'], command=self.toggle_ontop)
        self.switch_ontop.pack(side="left", padx=20)
        if self.cfg.get('always_on_top', '0') == '1':
            self.switch_ontop.select()

        # --- hotkeys ---
        self.f_hk = ctk.CTkFrame(self)
        self.f_hk.pack(fill="x", padx=20, pady=5, ipady=3)

        self.lbl_hk_title = ctk.CTkLabel(self.f_hk, text=t['hk_title'], font=("Arial", 12, "bold"))
        self.lbl_hk_title.grid(row=0, column=0, columnspan=5, padx=10, pady=2, sticky="w")

        self.lbl_hk_s = ctk.CTkLabel(self.f_hk, text=t['hk_start'])
        self.lbl_hk_s.grid(row=1, column=0, padx=10, pady=2)
        self.ent_hk_start = ctk.CTkEntry(self.f_hk, width=70)
        self.ent_hk_start.insert(0, self.cfg.get('start_key', 'f1'))
        self.ent_hk_start.grid(row=1, column=1, pady=2)

        self.lbl_hk_t = ctk.CTkLabel(self.f_hk, text=t['hk_stop'])
        self.lbl_hk_t.grid(row=1, column=2, padx=(15, 5), pady=2)
        self.ent_hk_stop = ctk.CTkEntry(self.f_hk, width=70)
        self.ent_hk_stop.insert(0, self.cfg.get('stop_key', 'f2'))
        self.ent_hk_stop.grid(row=1, column=3, pady=2)

        self.btn_hk_upd = ctk.CTkButton(self.f_hk, text=t['hk_btn'], width=90, command=self.action_update_hk)
        self.btn_hk_upd.grid(row=1, column=4, padx=20, pady=2)

        # --- status ---
        self.lbl_inline_err = ctk.CTkLabel(self, text="", text_color="#dc3545", font=("Arial", 12, "bold"))
        self.lbl_inline_err.pack(pady=(2, 0))

        self.lbl_status = ctk.CTkLabel(self, text=t['status_idle'], text_color="#ffc107", font=("Arial", 13, "bold"))
        self.lbl_status.pack()
        self.lbl_counter = ctk.CTkLabel(self, text=t['counter'].format(0, self.cfg.get('limit', '0')))
        self.lbl_counter.pack()
        self.lbl_warn = ctk.CTkLabel(self, text=t['warn'], text_color="#ffc107", font=("Arial", 11))
        self.lbl_warn.pack(pady=5)

    # ---------- helpers ----------

    def paste_text(self):
        self.txt_entry.delete("1.0", "end")
        self.txt_entry.insert("1.0", pyperclip.paste())

    def parse_hotkey(self, key_str):
        k = key_str.lower().strip()
        if not k:
            return ""
        if k.startswith("<") and ">" in k:
            return k
        if "+" in k:
            parts = [p.strip() for p in k.split("+") if p.strip()]
            return "+".join(f"<{p}>" if len(p) > 1 else p for p in parts)
        return f"<{k}>" if len(k) > 1 else k

    def hook_keys(self):
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except Exception:
                pass

        s_key = self.parse_hotkey(self.cfg.get('start_key', 'f1'))
        t_key = self.parse_hotkey(self.cfg.get('stop_key', 'f2'))

        try:
            hotkeys = {
                s_key: lambda: self.after(0, self.action_start),
                t_key: lambda: self.after(0, self.action_stop),
            }
            self.hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
            self.hotkey_listener.start()
        except Exception:
            self.lbl_inline_err.configure(text=config.TEXTS[self.cfg['lang']]['err_hk'])

    # ---------- toggles ----------

    def toggle_smooth_cfg(self):
        self.cfg['smooth_theme'] = '1' if self.switch_smooth.get() else '0'
        config.save_settings(self.cfg)

    def toggle_ontop(self):
        val = '1' if self.switch_ontop.get() else '0'
        self.cfg['always_on_top'] = val
        config.save_settings(self.cfg)
        self.attributes("-topmost", val == '1')

    def toggle_theme(self):
        self.cfg['theme'] = 'dark' if self.cfg.get('theme', 'dark') == 'light' else 'light'
        config.save_settings(self.cfg)
        self.btn_theme.configure(text="🌙" if self.cfg['theme'] == "light" else "☀️")

        if self.cfg.get('smooth_theme', '1') == '1':
            self.fade_out_theme(1.0)
        else:
            ctk.set_appearance_mode(self.cfg['theme'])
            self.update()

    def fade_out_theme(self, alpha):
        if alpha > 0.1:
            alpha -= 0.15
            self.attributes("-alpha", max(0.01, alpha))
            self.after(16, lambda: self.fade_out_theme(alpha))
        else:
            ctk.set_appearance_mode(self.cfg['theme'])
            self.update()
            self.fade_in_theme(0.01)

    def fade_in_theme(self, alpha):
        if alpha < 1.0:
            alpha += 0.15
            self.attributes("-alpha", min(1.0, alpha))
            self.after(16, lambda: self.fade_in_theme(alpha))
        else:
            self.attributes("-alpha", 1.0)

    def toggle_lang(self):
        self.cfg['lang'] = 'ru' if self.cfg.get('lang', 'en') == 'en' else 'en'
        config.save_settings(self.cfg)
        self.apply_texts()

    def apply_texts(self):
        t = config.TEXTS[self.cfg['lang']]
        self.btn_lang.configure(text="RU" if self.cfg['lang'] == "en" else "EN")
        self.lbl_spam.configure(text=t['spam_lbl'])
        self.btn_paste.configure(text=t['paste'])
        self.lbl_delay.configure(text=t['delay_lbl'])
        self.lbl_limit.configure(text=t['limit_lbl'])

        if self.core.is_running:
            self.lbl_status.configure(text=t['status_work'])
        elif self.btn_start.cget('state') == 'disabled':
            self.lbl_status.configure(text=t['status_stop'])
        else:
            self.lbl_status.configure(text=t['status_idle'])

        self.btn_start.configure(text=t['start'].format(self.cfg.get('start_key', 'f1').upper()))
        self.btn_stop.configure(text=t['stop'].format(self.cfg.get('stop_key', 'f2').upper()))

        self.lbl_sett_title.configure(text=t['sett_title'])
        self.switch_smooth.configure(text=t['sett_smooth'])
        self.switch_ontop.configure(text=t['sett_ontop'])

        self.lbl_hk_title.configure(text=t['hk_title'])
        self.lbl_hk_s.configure(text=t['hk_start'])
        self.lbl_hk_t.configure(text=t['hk_stop'])
        self.btn_hk_upd.configure(text=t['hk_btn'])
        self.lbl_counter.configure(text=t['counter'].format(self.core.msg_count, self.cfg.get('limit', '0')))
        self.lbl_warn.configure(text=t['warn'])

    # ---------- actions ----------

    def action_update_hk(self):
        sk = self.ent_hk_start.get().strip().lower()
        tk_ = self.ent_hk_stop.get().strip().lower()
        if not sk or not tk_:
            return
        if sk == tk_:
            self.lbl_inline_err.configure(text=config.TEXTS[self.cfg['lang']]['err_hk'])
            return

        try:
            test = keyboard.GlobalHotKeys({
                self.parse_hotkey(sk): lambda: None,
                self.parse_hotkey(tk_): lambda: None,
            })
            test.start()
            test.stop()
        except Exception:
            self.lbl_inline_err.configure(text=config.TEXTS[self.cfg['lang']]['err_hk'])
            return

        self.cfg['start_key'] = sk
        self.cfg['stop_key'] = tk_
        config.save_settings(self.cfg)
        self.hook_keys()
        self.lbl_inline_err.configure(text="")
        self.btn_start.configure(text=config.TEXTS[self.cfg['lang']]['start'].format(sk.upper()))
        self.btn_stop.configure(text=config.TEXTS[self.cfg['lang']]['stop'].format(tk_.upper()))

    def action_start(self):
        if self.core.is_running:
            return

        text = self.txt_entry.get("1.0", "end-1c")
        if not text.strip():
            self.lbl_inline_err.configure(text=config.TEXTS[self.cfg['lang']]['err_empty'])
            return

        try:
            delay = int(self.delay_entry.get())
        except ValueError:
            self.lbl_inline_err.configure(text=config.TEXTS[self.cfg['lang']]['err_delay'])
            return

        try:
            limit = int(self.limit_entry.get())
        except ValueError:
            self.lbl_inline_err.configure(text=config.TEXTS[self.cfg['lang']]['err_limit'])
            return

        self.lbl_inline_err.configure(text="")
        self.cfg['limit'] = str(limit)
        self.cfg['delay'] = str(delay)
        self.cfg['spam_text'] = text[:5000]
        config.save_settings(self.cfg)

        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")

        self.core.start(text, delay, limit)

    def action_stop(self):
        self.core.stop()

    # ---------- callbacks ----------

    def update_status_ui(self, status_type, val):
        t = config.TEXTS[self.cfg['lang']]
        if status_type == 'countdown':
            self.after(0, lambda: self.lbl_status.configure(
                text=t['status_countdown'].format(val), text_color="#ffc107"
            ))
        elif status_type == 'work':
            self.after(0, lambda: self.lbl_status.configure(
                text=t['status_work'], text_color="#28a745"
            ))

    def update_counter_ui(self, count):
        self.after(0, lambda: self.lbl_counter.configure(
            text=config.TEXTS[self.cfg['lang']]['counter'].format(count, self.cfg.get('limit', '0'))
        ))

    def spam_finished_ui(self):
        self.after(0, lambda: [
            self.btn_start.configure(state="normal"),
            self.btn_stop.configure(state="disabled"),
            self.lbl_status.configure(
                text=config.TEXTS[self.cfg['lang']]['status_stop'], text_color="#dc3545"
            ),
        ])

    def on_closing(self):
        if hasattr(self, 'watchdog'):
            self.watchdog.stop()
        self.core.stop()
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except Exception:
                pass
        try:
            if os.path.exists(self._pid_file):
                os.remove(self._pid_file)
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()