@echo off
title Remove CustomerVault from Startup
cd /d "%~dp0"

set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\CustomerVault.lnk"

if exist "%SHORTCUT_PATH%" (
    del /f /q "%SHORTCUT_PATH%"
    echo CustomerVault has been removed from Windows Startup.
) else (
    echo CustomerVault is not currently in Windows Startup.
)

pause
