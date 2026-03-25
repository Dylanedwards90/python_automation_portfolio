@echo off
title Job Lead Monitor - Watching Input Folder
cd /d "%~dp0"

:loop
echo [%date% %time%] Checking for New CSV files...
echo.

py main.py


timeout /t 10 /nobreak >nul
goto loop