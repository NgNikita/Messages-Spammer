import sys
from tkinter import messagebox
import customtkinter as ctk
import keyboard
import pyperclip

import config
from spammer import SpammerCore

try:
    import keyboard
    import pyperclip
except ImportError:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Run run.bat first to install modules!")
    sys.exit(1)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.cfg = config.load_settings()
        
        ctk.set_appearance_mode(self.cfg['theme'])
        ctk.set_default_color_theme("blue")
        
        self.title("(M-S) Messages Spammer")
        self.geometry("520x630")
        self.resizable(False, False)
        
        self.attributes("-topmost", self.cfg.get('always_on_top', '0') == '1')
        
        self.hk_start_ref = None
        self.hk_stop_ref = None
        
        self.core = SpammerCore(self.update_counter_ui, self.spam_finished_ui)
        
        self.init_ui()
        self.hook_keys()

    def init_ui(self):
        lang = self.cfg['lang']
        t = config.TEXTS[lang]
        
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(15, 0))
        
        self.btn_lang = ctk.CTkButton(self.top_frame, text="RU" if lang == "en" else "EN", width=60, command=self.toggle_lang)
        self.btn_lang.pack(side="left")
        
        self.btn_theme = ctk.CTkButton(self.top_frame, text="🌙" if self.cfg['theme'] == "light" else "☀️", width=60, command=self.toggle_theme)
        self.btn_theme.pack(side="left", padx=10)

        self.lbl_spam = ctk.CTkLabel(self, text=t['spam_lbl'])
        self.lbl_spam.pack(anchor="w", padx=20, pady=(15, 0))
        
        self.f_entry = ctk.CTkFrame(self, fg_color="transparent")
        self.f_entry.pack(fill="x", padx=20, pady=5)
        self.txt_entry = ctk.CTkEntry(self.f_entry, placeholder_text="...")
        self.txt_entry.pack(side="left", fill="x", expand=True)
        self.btn_paste = ctk.CTkButton(self.f_entry, text=t['paste'], width=70, command=lambda: [self.txt_entry.delete(0, 'end'), self.txt_entry.insert(0, pyperclip.paste())])
        self.btn_paste.pack(side="right", padx=(5, 0))

        self.lbl_delay = ctk.CTkLabel(self, text=t['delay_lbl'])
        self.lbl_delay.pack(anchor="w", padx=20, pady=(10, 0))
        self.delay_entry = ctk.CTkEntry(self)
        self.delay_entry.insert(0, "1000")
        self.delay_entry.pack(fill="x", padx=20, pady=5)

        self.lbl_limit = ctk.CTkLabel(self, text=t['limit_lbl'])
        self.lbl_limit.pack(anchor="w", padx=20, pady=(10, 0))
        self.limit_entry = ctk.CTkEntry(self)
        self.limit_entry.insert(0, self.cfg['limit'])
        self.limit_entry.pack(fill="x", padx=20, pady=5)

        self.f_control = ctk.CTkFrame(self, fg_color="transparent")
        self.f_control.pack(pady=5)
        self.btn_start = ctk.CTkButton(self.f_control, text=t['start'].format(self.cfg['start_key'].upper()), fg_color="#28a745", hover_color="#218838", command=self.action_start)
        self.btn_start.pack(side="left", padx=10)
        self.btn_stop = ctk.CTkButton(self.f_control, text=t['stop'].format(self.cfg['stop_key'].upper()), fg_color="#dc3545", hover_color="#c82333", state="disabled", command=self.action_stop)
        self.btn_stop.pack(side="left", padx=10)

        self.f_sett = ctk.CTkFrame(self)
        self.f_sett.pack(fill="x", padx=20, pady=5, ipady=5)
        
        self.lbl_sett_title = ctk.CTkLabel(self.f_sett, text=t['sett_title'], font=("Arial", 12, "bold"))
        self.lbl_sett_title.pack(anchor="w", padx=10, pady=5)
        
        self.f_sett_inner = ctk.CTkFrame(self.f_sett, fg_color="transparent")
        self.f_sett_inner.pack(fill="x", padx=10, pady=2)
        
        self.switch_smooth = ctk.CTkSwitch(self.f_sett_inner, text=t['sett_smooth'], command=self.toggle_smooth_cfg)
        self.switch_smooth.pack(side="left", padx=5)
        if self.cfg.get('smooth_theme', '1') == '1': self.switch_smooth.select()
        
        self.switch_ontop = ctk.CTkSwitch(self.f_sett_inner, text=t['sett_ontop'], command=self.toggle_ontop)
        self.switch_ontop.pack(side="left", padx=20)
        if self.cfg.get('always_on_top', '0') == '1': self.switch_ontop.select()

        self.f_hk = ctk.CTkFrame(self)
        self.f_hk.pack(fill="x", padx=20, pady=5, ipady=5)
        
        self.lbl_hk_title = ctk.CTkLabel(self.f_hk, text=t['hk_title'], font=("Arial", 12, "bold"))
        self.lbl_hk_title.grid(row=0, column=0, columnspan=5, padx=10, pady=5, sticky="w")
        
        self.lbl_hk_s = ctk.CTkLabel(self.f_hk, text=t['hk_start'])
        self.lbl_hk_s.grid(row=1, column=0, padx=10, pady=5)
        self.ent_hk_start = ctk.CTkEntry(self.f_hk, width=70)
        self.ent_hk_start.insert(0, self.cfg['start_key'])
        self.ent_hk_start.grid(row=1, column=1, pady=5)

        self.lbl_hk_t = ctk.CTkLabel(self.f_hk, text=t['hk_stop'])
        self.lbl_hk_t.grid(row=1, column=2, padx=(15, 5), pady=5)
        self.ent_hk_stop = ctk.CTkEntry(self.f_hk, width=70)
        self.ent_hk_stop.insert(0, self.cfg['stop_key'])
        self.ent_hk_stop.grid(row=1, column=3, pady=5)

        self.btn_hk_upd = ctk.CTkButton(self.f_hk, text=t['hk_btn'], width=90, command=self.action_update_hk)
        self.btn_hk_upd.grid(row=1, column=4, padx=20, pady=5)

        self.lbl_inline_err = ctk.CTkLabel(self, text="", text_color="#dc3545", font=("Arial", 12, "bold"))
        self.lbl_inline_err.pack(pady=(2, 0))

        self.lbl_status = ctk.CTkLabel(self, text=t['status_idle'], text_color="#ffc107", font=("Arial", 13, "bold"))
        self.lbl_status.pack()
        self.lbl_counter = ctk.CTkLabel(self, text=t['counter'].format(0, self.cfg['limit']))
        self.lbl_counter.pack()
        self.lbl_warn = ctk.CTkLabel(self, text=t['warn'], text_color="#ffc107", font=("Arial", 11))
        self.lbl_warn.pack(pady=5)

        vcmd = (self.register(self.validate_digits), '%P')
        self.delay_entry._entry.configure(validate="key", validatecommand=vcmd)
        self.limit_entry._entry.configure(validate="key", validatecommand=vcmd)

        for e in (self.txt_entry, self.delay_entry, self.limit_entry, self.ent_hk_start, self.ent_hk_stop):
            e._entry.bind("<Control-a>", self.select_all)
            e._entry.bind("<Control-A>", self.select_all)

    def validate_digits(self, P):
        if P == "" or P.isdigit():
            self.lbl_inline_err.configure(text="")
            return True
        return False

    def select_all(self, event):
        event.widget.select_range(0, 'end')
        event.widget.icursor('end')
        return "break"

    def hook_keys(self):
        try:
            if self.hk_start_ref:
                try: keyboard.remove_hotkey(self.hk_start_ref)
                except: pass
            if self.hk_stop_ref:
                try: keyboard.remove_hotkey(self.hk_stop_ref)
                except: pass
            self.hk_start_ref = keyboard.add_hotkey(self.cfg['start_key'], self.action_start)
            self.hk_stop_ref = keyboard.add_hotkey(self.cfg['stop_key'], self.action_stop)
        except Exception as e:
            if "blocking_hotkeys" not in str(e):
                self.lbl_inline_err.configure(text=f"Hotkey Error: {e}")

    def toggle_smooth_cfg(self):
        self.cfg['smooth_theme'] = '1' if self.switch_smooth.get() else '0'
        config.save_settings(self.cfg)

    def toggle_ontop(self):
        val = '1' if self.switch_ontop.get() else '0'
        self.cfg['always_on_top'] = val
        config.save_settings(self.cfg)
        self.attributes("-topmost", val == '1')

    def toggle_theme(self):
        self.cfg['theme'] = 'dark' if self.cfg['theme'] == 'light' else 'light'
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
        self.cfg['lang'] = 'ru' if self.cfg['lang'] == 'en' else 'en'
        config.save_settings(self.cfg)
        
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
            
        self.btn_start.configure(text=t['start'].format(self.cfg['start_key'].upper()))
        self.btn_stop.configure(text=t['stop'].format(self.cfg['stop_key'].upper()))
        
        self.lbl_sett_title.configure(text=t['sett_title'])
        self.switch_smooth.configure(text=t['sett_smooth'])
        self.switch_ontop.configure(text=t['sett_ontop'])
        
        self.lbl_hk_title.configure(text=t['hk_title'])
        self.lbl_hk_s.configure(text=t['hk_start'])
        self.lbl_hk_t.configure(text=t['hk_stop'])
        self.btn_hk_upd.configure(text=t['hk_btn'])
        self.lbl_counter.configure(text=t['counter'].format(self.core.msg_count, self.cfg['limit']))
        self.lbl_warn.configure(text=t['warn'])

    def action_update_hk(self):
        sk = self.ent_hk_start.get().strip().lower()
        tk_key = self.ent_hk_stop.get().strip().lower()
        if not sk or not tk_key: return
        self.cfg['start_key'] = sk
        self.cfg['stop_key'] = tk_key
        config.save_settings(self.cfg)
        self.hook_keys()
        self.btn_start.configure(text=config.TEXTS[self.cfg['lang']]['start'].format(sk.upper()))
        self.btn_stop.configure(text=config.TEXTS[self.cfg['lang']]['stop'].format(tk_key.upper()))

    def action_start(self):
        text = self.txt_entry.get()
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
        config.save_settings(self.cfg)
        
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.lbl_status.configure(text=config.TEXTS[self.cfg['lang']]['status_work'], text_color="#28a745")
        
        self.core.start(text, delay, limit)

    def action_stop(self):
        self.core.stop()

    def update_counter_ui(self, count):
        self.after(0, lambda: self.lbl_counter.configure(text=config.TEXTS[self.cfg['lang']]['counter'].format(count, self.cfg['limit'])))

    def spam_finished_ui(self):
        self.after(0, lambda: [
            self.btn_start.configure(state="normal"),
            self.btn_stop.configure(state="disabled"),
            self.lbl_status.configure(text=config.TEXTS[self.cfg['lang']]['status_stop'], text_color="#dc3545")
        ])

    def on_closing(self):
        self.core.stop()
        if self.hk_start_ref:
            try: keyboard.remove_hotkey(self.hk_start_ref)
            except: pass
        if self.hk_stop_ref:
            try: keyboard.remove_hotkey(self.hk_stop_ref)
            except: pass
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()