@echo off
rem Windows launcher: use Python if available, otherwise fall back to PowerShell version
where pyw >nul 2>nul
if %errorlevel%==0 (
    start "" pyw "%~dp0alcom_path_changer.py"
    exit /b
)
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%~dp0alcom_path_changer.py"
    exit /b
)
start "" powershell -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File "%~dp0ALCOM_PathChanger.ps1"
