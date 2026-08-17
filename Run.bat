@echo off
chcp 65001 >nul
title Cursor Local Provider Unlocker - by DerminDeep
cd /d "%~dp0"

python -c "import customtkinter" 2>nul
if %errorlevel% neq 0 (
    echo [DerminDeep] Installing customtkinter...
    pip install customtkinter
)

start "" pythonw app.py
