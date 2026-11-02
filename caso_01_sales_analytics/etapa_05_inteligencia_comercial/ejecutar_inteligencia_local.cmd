@echo off
setlocal
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (echo ERROR: falta .venv en V17 & exit /b 1)
".venv\Scripts\python.exe" "etapa_05_inteligencia_comercial\python\motor_comercial.py" --local
exit /b %errorlevel%
