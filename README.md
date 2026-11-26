# (M-S) Messages Spammer

> **Quick Start · End-User Notice · Disclaimer · Terms of Use**  
> **Languages:** [English](#en---english) | [Русский](#ru---русский)

Local desktop utility that automates typing and sending text into an input field of an already-open third-party application.

---

## EN - ENGLISH

### 0. Quick Start

* Run `START.bat` to install dependencies (`customtkinter`, `pynput`, `pyperclip`) and launch the app, or run `main.py` directly with Python.
* Enter text, delay (`ms`), and message limit (`0` = unlimited), focus the target input field, then press **Start** or the start hotkey (default: `F1`).
* Stop anytime via the **Stop** button, the stop hotkey (default: `F2`), or `Emergency Stop.bat`.
* Settings are saved automatically to `config.txt`.

| File / Control | Purpose |
| :--- | :--- |
| `START.bat` / `main.py` | Install dependencies (`.bat`) and launch the GUI application |
| `Emergency Stop.bat` | Emergency termination script using `app.pid` (with fallback kill) |
| `config.txt` / `config.py` | Persistent configuration and validation |
| `spammer.py` / `watchdog.py` | Core input automation loop and process/file watchdog |

### 1. What This Program Is

**"(M-S) Messages Spammer"** is a local desktop utility that automates typing and sending text into an input field of an already-open third-party application (chat, messenger, form, test page, etc.).

The program:

* does **NOT** connect to any network on its own;
* does **NOT** bypass authentication or access controls;
* does **NOT** interact with any remote service directly;
* only simulates keyboard input on your own machine.

It is intended for:

* personal automation of repetitive text entry;
* testing and debugging your own chats, bots, or forms;
* educational review of GUI automation techniques;
* accessibility scenarios where manual typing is difficult.

### 2. Acceptable Use

You agree to use this program **ONLY** in ways that are legal in your jurisdiction and that comply with:

* the terms of service of every application you interact with;
* the rules of any chat, community, or platform you use it on;
* anti-spam and computer-misuse legislation applicable to you.

> [!WARNING]
> You **MUST NOT** use this program to:
> * send unsolicited bulk messages (spam), advertisements, scams, or chain letters;
> * harass, threaten, stalk, or abuse any person;
> * flood, DoS, or otherwise degrade any service or chat;
> * impersonate any person or organisation;
> * distribute malware, phishing links, or illegal content;
> * circumvent rate limits, bans, or access controls;
> * violate any applicable law or regulation.

The word *"Spammer"* in the name describes the technical function (automated repeated text entry). It is not an endorsement of abusive messaging. Any misuse is the sole responsibility of the user.

### 3. No Warranty

THE PROGRAM IS PROVIDED **"AS IS"**, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND NON-INFRINGEMENT.

The author does not warrant that:

* the program will work with any specific application, operating system, keyboard layout, or language;
* the program will be error-free, uninterrupted, or secure;
* any particular result will be achieved by using it.

### 4. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE AUTHOR SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO:

* loss of data, messages, accounts, or profiles;
* account bans, restrictions, or suspensions by any service;
* system failures, crashes, freezes, or data corruption;
* loss of profits, revenue, goodwill, or business;
* any other harm or loss arising out of or in connection with the use of, or inability to use, this program,

even if the author has been advised of the possibility of such damages. This applies regardless of the legal theory (contract, tort, negligence, strict liability, or otherwise).

### 5. User Responsibility and Indemnification

You use this program entirely at your own risk.

You are solely responsible for:

* the content you send and the targets you send it to;
* compliance with all applicable laws and third-party terms;
* any consequences on your accounts, devices, or network;
* keeping backups of any data you care about.

You agree to indemnify and hold harmless the author from any claim, demand, damage, loss, or expense (including reasonable legal fees) arising from your use or misuse of the program or your breach of this notice.

### 6. Eligibility

By using this program you confirm that:

* you are of legal age in your jurisdiction, or have the consent of a parent or legal guardian;
* you have the legal capacity to enter into this notice;
* you have read and understood it in full.

If you do not agree with any part of this notice, do not use the program and delete it from your device.

### 7. Third-Party Components

The program depends on third-party open-source libraries (for example: `customtkinter`, `pynput`, `pyperclip`). Those libraries are governed by their own licenses, which apply to them independently of this notice. This notice does not modify or replace those licenses.

### 8. No Support, No Update Guarantee

The author is under no obligation to provide support, updates, fixes, or new features. Any assistance is provided voluntarily and without warranty.

### 9. Changes to This Notice

This notice may be updated at any time. The version shipped with the program is the version that applies to your copy. Continued use after an update constitutes acceptance of the updated notice.

### 10. Severability

If any provision of this notice is held to be invalid or unenforceable, the remaining provisions shall remain in full force and effect.

> [!IMPORTANT]
> By installing, running, or otherwise using **"(M-S) Messages Spammer"**, you acknowledge that you have read, understood, and agreed to all of the above.

---

## RU - РУССКИЙ

### 0. Быстрый старт

* Запустите `START.bat` для установки зависимостей (`customtkinter`, `pynput`, `pyperclip`) и запуска приложения либо запустите `main.py` напрямую через Python.
* Введите текст, задержку (`мс`) и лимит сообщений (`0` = безлимит), кликните в нужное поле ввода и нажмите **«Старт»** или горячую клавишу запуска (по умолчанию `F1`).
* Остановить отправку можно кнопкой **«Стоп»**, горячей клавишей остановки (по умолчанию `F2`) или через `Emergency Stop.bat`.
* Настройки автоматически сохраняются в `config.txt`.

| Файл / элемент | Назначение |
| :--- | :--- |
| `START.bat` / `main.py` | Установка зависимостей (`.bat`) и запуск графического интерфейса |
| `Emergency Stop.bat` | Аварийная остановка процесса по `app.pid` (с резервным завершением) |
| `config.txt` / `config.py` | Хранение и валидация настроек |
| `spammer.py` / `watchdog.py` | Логика отправки и контроль целостности/отклика |

### 1. Что это за программа

**"(M-S) Messages Spammer"** — локальная настольная утилита, автоматизирующая ввод и отправку текста в поле ввода уже открытого стороннего приложения (чат, мессенджер, форма, тестовая страница и т.п.).

Программа:

* **НЕ** подключается к сети самостоятельно;
* **НЕ** обходит аутентификацию и механизмы контроля доступа;
* **НЕ** обращается к удалённым сервисам напрямую;
* только эмулирует ввод с клавиатуры на вашей машине.

Программа предназначена для:

* личной автоматизации повторяющегося ввода текста;
* тестирования и отладки собственных чатов, ботов, форм;
* ознакомления с методами автоматизации GUI;
* сценариев доступности, где ручной ввод затруднён.

### 2. Допустимое использование

Вы обязуетесь использовать программу **ТОЛЬКО** способами, которые законны в вашей юрисдикции и соответствуют:

* условиям использования каждого приложения, с которым вы взаимодействуете;
* правилам любого чата, сообщества или платформы, где вы её применяете;
* законодательству о спаме и о неправомерном доступе к компьютерной информации, применимому к вам.

> [!WARNING]
> Вам **ЗАПРЕЩАЕТСЯ** использовать программу для:
> * рассылки нежелательных массовых сообщений (спама), рекламы, мошеннических схем или «писем счастья»;
> * преследования, угроз, сталкинга или оскорблений любого лица;
> * флуда, DoS-атак или иной деградации сервиса/чата;
> * выдачи себя за другое лицо или организацию;
> * распространения вредоносного ПО, фишинговых ссылок или противоправного контента;
> * обхода ограничений частоты, блокировок или средств контроля доступа;
> * нарушения любого применимого закона или нормативного акта.

Слово *«Spammer»* в названии описывает техническую функцию (автоматизированный повторяющийся ввод текста) и не является одобрением злоупотреблений. Вся ответственность за злоупотребление лежит на пользователе.

### 3. Отсутствие гарантий

ПРОГРАММА ПРЕДОСТАВЛЯЕТСЯ **«КАК ЕСТЬ» (AS IS)**, БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ, ПОМИМО ПРОЧЕГО, ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, ПРИГОДНОСТИ ДЛЯ КОНКРЕТНОЙ ЦЕЛИ, ПРАВОВОГО ТИТУЛА И НЕНАРУШЕНИЯ ПРАВ ТРЕТЬИХ ЛИЦ.

Автор не гарантирует, что:

* программа будет работать с конкретным приложением, ОС, раскладкой клавиатуры или языком;
* программа будет безошибочной, бесперебойной и защищённой;
* использование программы приведёт к какому-либо конкретному результату.

### 4. Ограничение ответственности

В МАКСИМАЛЬНОЙ СТЕПЕНИ, РАЗРЕШЁННОЙ ПРИМЕНИМЫМ ПРАВОМ, АВТОР НЕ НЕСЁТ ОТВЕТСТВЕННОСТИ ЗА ЛЮБЫЕ ПРЯМЫЕ, КОСВЕННЫЕ, СЛУЧАЙНЫЕ, ОСОБЫЕ, ШТРАФНЫЕ ИЛИ ПОСЛЕДУЮЩИЕ УБЫТКИ, ВКЛЮЧАЯ, ПОМИМО ПРОЧЕГО:

* потерю данных, сообщений, аккаунтов или профилей;
* блокировки, ограничения или приостановки аккаунтов любым сервисом;
* сбои системы, зависания, падения или повреждение данных;
* упущенную выгоду, утрату дохода, деловой репутации или бизнеса;
* любой иной вред или убытки, возникшие в связи с использованием или невозможностью использования программы,

даже если автор был предупреждён о возможности таких убытков. Это применяется независимо от правовой теории (договор, деликт, небрежность, строгая ответственность и т.п.).

### 5. Ответственность пользователя и возмещение

Вы используете программу исключительно на свой страх и риск.

Вы несёте единоличную ответственность за:

* контент, который вы отправляете, и адресатов, кому вы его отправляете;
* соблюдение всех применимых законов и правил третьих лиц;
* любые последствия для ваших аккаунтов, устройств и сети;
* создание резервных копий важных для вас данных.

Вы обязуетесь возместить автору и оградить его от любых претензий, требований, убытков, потерь и расходов (включая разумные судебные издержки), возникших из-за вашего использования или неправомерного использования программы либо нарушения этого уведомления.

### 6. Правоспособность

Используя программу, вы подтверждаете, что:

* достигли совершеннолетия в своей юрисдикции либо получили согласие родителя или опекуна;
* обладаете необходимой правоспособностью для принятия этого уведомления;
* полностью прочитали и поняли его.

Если вы не согласны с какой-либо частью уведомления, не используйте программу и удалите её со своего устройства.

### 7. Сторонние компоненты

Программа зависит от сторонних open-source библиотек (например: `customtkinter`, `pynput`, `pyperclip`). Эти библиотеки регулируются их собственными лицензиями, которые применяются к ним независимо от настоящего уведомления. Настоящее уведомление не изменяет и не заменяет эти лицензии.

### 8. Без поддержки и гарантий обновлений

Автор не обязан предоставлять поддержку, обновления, исправления или новые функции. Любая помощь оказывается добровольно и без каких-либо гарантий.

### 9. Изменение уведомления

Уведомление может быть обновлено в любое время. К вашей копии применяется та версия, которая поставляется вместе с ней. Продолжение использования после обновления означает принятие обновлённого уведомления.

### 10. Делимость положений

Если какое-либо положение уведомления будет признано недействительным или неисполнимым, остальные положения сохраняют полную силу и действие.

> [!IMPORTANT]
> Устанавливая, запуская или иным образом используя **"(M-S) Messages Spammer"**, вы подтверждаете, что прочитали, поняли и принимаете всё вышеизложенное.
