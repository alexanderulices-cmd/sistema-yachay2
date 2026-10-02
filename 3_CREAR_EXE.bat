@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Creando SistemaYachay.exe (puede tardar 5-15 minutos, no cierre la ventana)...
python -m PyInstaller --noconfirm --clean yachay.spec
if errorlevel 1 (echo. & echo ERROR al compilar. Copie el texto de arriba y enviemelo. & pause & exit /b 1)
echo.
echo Compilado. Ejecutando AUTOPRUEBA del programa...
set YACHAY_SELFTEST=1
dist\SistemaYachay\SistemaYachay.exe
set YACHAY_SELFTEST=
echo.
echo Si arriba dice "SELFTEST exceptions: []" todo esta correcto.
echo El programa esta en:  dist\SistemaYachay\SistemaYachay.exe
echo Copie TODA la carpeta dist\SistemaYachay a cualquier PC (no necesita Python).
pause
