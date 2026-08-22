@echo off
title Cricket Match Stats Manager

echo =====================================
echo   Cricket Match Stats Manager
echo =====================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running project...
python main.py

echo.
echo =====================================
echo   Project finished
echo =====================================
echo.

pause
