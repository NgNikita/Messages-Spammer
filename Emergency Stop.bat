@echo off
title Emergency Stop - Messages Spammer
set "PIDFILE=%~dp0app.pid"

if not exist "%PIDFILE%" (
    echo [WARN] app.pid not found. Trying fallback...
    goto :fallback
)

set /p PID=<"%PIDFILE%"
if "%PID%"=="" goto :fallback

echo Terminating process PID=%PID%...
taskkill /f /pid %PID% >nul 2>&1
del "%PIDFILE%" >nul 2>&1
echo [ SUCCESS ] App stopped (PID %PID%).
timeout /t 2 >nul
exit /b 0

:fallback
echo [WARN] Falling back to python.exe / pythonw.exe kill.
echo        This will also stop OTHER python scripts if any are running.
taskkill /f /im pythonw.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
echo [ SUCCESS ] All python processes terminated.
timeout /t 2 >nul
exit /b 0