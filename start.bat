@echo off
title CustomerVault - Fast Customer Directory
cd /d "%~dp0"

echo ===================================================
echo             Starting CustomerVault...
echo ===================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in your PATH.
    echo Please ensure Python is installed and added to PATH.
    pause
    exit /b 1
)

python server.py
if %errorlevel% neq 0 (
    echo.
    echo Server exited with an error.
    pause
)
