@echo off
title Install CustomerVault Permanent Background Startup
cd /d "%~dp0"

echo =========================================================
echo    Installing CustomerVault as a Permanent Windows Service
echo =========================================================
echo.

set "VBS_PATH=%~dp0run_background.vbs"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\CustomerVault.lnk"

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; " ^
  "$s = $ws.CreateShortcut('%SHORTCUT_PATH%'); " ^
  "$s.TargetPath = 'wscript.exe'; " ^
  "$s.Arguments = '\"%VBS_PATH%\"'; " ^
  "$s.WorkingDirectory = '%~dp0'; " ^
  "$s.Description = 'CustomerVault Background Service'; " ^
  "$s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo [SUCCESS] CustomerVault is now set to start automatically every time your PC turns on!
    echo.
    echo Starting the background server right now...
    wscript.exe "%VBS_PATH%"
    echo.
    echo CustomerVault is now running permanently in the background.
    echo You do not need to keep any black command prompt window open!
) else (
    echo [ERROR] Could not create startup shortcut.
)

echo.
pause
