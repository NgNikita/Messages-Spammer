@echo off
title Launching (M-S) Messages Spammer

:: Автоматическая проверка и установка библиотек (тихий режим)
echo Checking and installing required libraries...
pip install customtkinter keyboard pyperclip --quiet

:: Запуск приложения через pythonw (скрывает консоль Python)
echo Starting app...
start "" pythonw main.py

:: Мгновенное закрытие окна самого bat-файла
exit