import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")

DEFAULT_CONFIG = {
    'lang': 'en',
    'theme': 'light',
    'start_key': 'f1',
    'stop_key': 'f2',
    'limit': '0',
    'smooth_theme': '1',
    'always_on_top': '0'
}

TEXTS = {
    'en': {
        'spam_lbl': 'Spam Text:', 'delay_lbl': 'Delay (ms):',
        'limit_lbl': 'Message Limit (0 = Infinite):', 'paste': 'Paste', 'start': 'Start ({})',
        'stop': 'Stop ({})', 'hk_title': ' Hotkeys ', 'hk_start': 'Start:', 'hk_stop': 'Stop:',
        'hk_btn': 'Update', 'status_idle': 'Idle', 'status_work': 'SPAMMING...',
        'status_stop': 'Stopped', 'counter': 'Sent: {} / {}', 'warn': 'Click on Telegram input first!',
        'err_empty': 'Error: Enter spam text!', 
        'err_delay': 'Error: Delay field cannot be empty!', 
        'err_limit': 'Error: Limit field cannot be empty!',
        'sett_title': ' Settings ', 'sett_smooth': 'Smooth Theme Animation', 'sett_ontop': 'Always on Top'
    },
    'ru': {
        'spam_lbl': 'Текст спама:', 'delay_lbl': 'Задержка (мс):',
        'limit_lbl': 'Лимит сообщений (0 = Безлимит):', 'paste': 'Вставить', 'start': 'Старт ({})',
        'stop': 'Стоп ({})', 'hk_title': ' Горячие клавиши ', 'hk_start': 'Старт:', 'hk_stop': 'Стоп:',
        'hk_btn': 'Обновить', 'status_idle': 'Пауза', 'status_work': 'Спам',
        'status_stop': 'Остановлен', 'counter': 'Отправлено: {} / {}', 'warn': 'Кликни в поле ввода Телеграма!',
        'err_empty': 'Ошибка: Введите текст для отправки!', 
        'err_delay': 'Ошибка: Поле задержки не может быть пустым!', 
        'err_limit': 'Ошибка: Поле лимита не может быть пустым!',
        'sett_title': ' Настройки ', 'sett_smooth': 'Плавная смена темы', 'sett_ontop': 'Поверх всех окон'
    }
}

def load_settings():
    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        k, v = line.strip().split('=', 1)
                        if k in cfg: cfg[k] = v
        except: pass
    return cfg

def save_settings(cfg):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            for k, v in cfg.items(): f.write(f"{k}={v}\n")
    except: pass