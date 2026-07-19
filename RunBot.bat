@echo off
:: Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :admin
) else (
    goto :get_admin
)

:get_admin
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b

:admin
cd /d "%~dp0"
python main.py
pause
