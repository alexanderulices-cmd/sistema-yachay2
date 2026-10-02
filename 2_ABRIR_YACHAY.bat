@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Abriendo el Sistema Yachay en su navegador... (no cierre esta ventana)
python yachay_launcher.py
pause
