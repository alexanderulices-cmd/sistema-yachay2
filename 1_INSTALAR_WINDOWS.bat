@echo off
chcp 65001 >nul
echo ===============================================
echo   SISTEMA YACHAY - Instalacion en Windows
echo ===============================================
echo Necesita Python 3.11 instalado (python.org) con la opcion "Add to PATH".
python --version || (echo ERROR: Python no esta instalado o no esta en el PATH & pause & exit /b 1)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
echo.
echo Instalacion terminada. Ahora use 2_ABRIR_YACHAY.bat
pause
