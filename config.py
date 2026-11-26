import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")

DEFAULT_CONFIG = {
    'lang': 'en',
    'theme': 'dark',
    'start_key': 'f1',
    'stop_key': 'f2',
    'limit': '0',
    'delay': '1000',
    'spam_text': '',
    'smooth_theme': '1',
    'always_on_top': '0'
}

VALID_VALUES = {
    'lang': ['en', 'ru'],
    'theme': ['dark', 'light'],
    'smooth_theme': ['0', '1'],
    'always_on_top': ['0', '1']
}

TEXTS = {
    'en': {
        'spam_lbl': 'Spam Text:',
        'delay_lbl': 'Delay (ms):',
        'limit_lbl': 'Message Limit (0 = Infinite):',
        'paste': 'Paste',
        'start': 'Start ({})',
        'stop': 'Stop ({})',
        'hk_title': ' Hotkeys ',
        'hk_start': 'Start:',
        'hk_stop': 'Stop:',
        'hk_btn': 'Update',
        'status_idle': 'Idle',
        'status_countdown': 'Starting in {}s.. Click target field',
        'status_work': 'Spamming',
        'status_stop': 'Stopped',
        'counter': 'Sent: {} / {}',
        'warn': 'Click on input',
        'err_empty': 'Error: Enter spam text',
        'err_delay': 'Error: Delay field cannot be empty',
        'err_limit': 'Error: Limit field cannot be empty',
        'err_hk': 'Hotkey registration failed! Run as admin if needed.',
        'sett_title': ' Settings ',
        'sett_smooth': 'Smooth Theme Animation',
        'sett_ontop': 'Always on Top'
    },
    'ru': {
        'spam_lbl': 'Текст спама:',
        'delay_lbl': 'Задержка (мс):',
        'limit_lbl': 'Лимит сообщений (0 = Безлимит):',
        'paste': 'Вставить',
        'start': 'Старт ({})',
        'stop': 'Стоп ({})',
        'hk_title': ' Горячие клавиши ',
        'hk_start': 'Старт:',
        'hk_stop': 'Стоп:',
        'hk_btn': 'Обновить',
        'status_idle': 'Пауза',
        'status_countdown': 'Запуск через {}с.. Кликни в поле ввода',
        'status_work': 'Спам',
        'status_stop': 'Остановлен',
        'counter': 'Отправлено: {} / {}',
        'warn': 'Кликни в поле ввода',
        'err_empty': 'Ошибка: Введите текст для отправки',
        'err_delay': 'Ошибка: Поле задержки не может быть пустым',
        'err_limit': 'Ошибка: Поле лимита не может быть пустым',
        'err_hk': 'Ошибка горячих клавиш! Запустите от имени админа.',
        'sett_title': ' Настройки ',
        'sett_smooth': 'Плавная смена темы',
        'sett_ontop': 'Поверх всех окон'
    }
}


def _normalize_non_negative_int(value: str) -> str | None:
    """Возвращает нормализованную строку с числом (без ведущих нулей),
    либо None, если значение не является неотрицательным целым."""
    if not value.isdigit():
        return None
    # "005" -> "5", "000" -> "0"
    return str(int(value))


def validate_config(cfg):
    repaired = False
    for key, default_val in DEFAULT_CONFIG.items():
        if key not in cfg:
            cfg[key] = default_val
            repaired = True
            continue

        if key in VALID_VALUES and cfg[key] not in VALID_VALUES[key]:
            cfg[key] = default_val
            repaired = True

        # limit и delay — только неотрицательные целые, без ведущих нулей
        if key in ('limit', 'delay'):
            normalized = _normalize_non_negative_int(cfg[key])
            if normalized is None:
                cfg[key] = default_val
                repaired = True
            elif normalized != cfg[key]:
                cfg[key] = normalized
                repaired = True

        if key in ('start_key', 'stop_key'):
            if not isinstance(cfg[key], str) or not cfg[key].strip():
                cfg[key] = default_val
                repaired = True

    return cfg, repaired


def load_settings():
    cfg = DEFAULT_CONFIG.copy()
    need_save = False

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        k, v = line.strip().split('=', 1)
                        cfg[k] = v
        except Exception:
            need_save = True
    else:
        need_save = True

    cfg, repaired = validate_config(cfg)

    if need_save or repaired:
        save_settings(cfg)

    return cfg


def save_settings(cfg):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            for k, v in cfg.items():
                f.write(f"{k}={v}\n")
    except Exception:
        pass