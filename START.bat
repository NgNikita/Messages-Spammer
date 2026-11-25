@echo off
title Launching (M-S) Messages Spammer
echo Checking and installing required libraries...
pip install customtkinter pynput pyperclip --quiet
echo Starting app...
start "" pythonw main.py
exit