@echo off
title Stop CustomerVault Server
cd /d "%~dp0"

echo Stopping CustomerVault background server...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*server.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host 'Killed process' $_.ProcessId }"
echo.
echo CustomerVault has been stopped.
pause
