@echo off
title Emergency Stop - Messages Spammer
echo Terminating all running Python instances...
taskkill /f /im pythonw.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
echo.
echo [ SUCCESS ] All background scripts have been forcefully stopped!
timeout /t 2 >nul
exit