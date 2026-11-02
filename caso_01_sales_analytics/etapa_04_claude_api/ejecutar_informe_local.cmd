@echo off
setlocal
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv no existe en la carpeta raiz de V16.
  exit /b 1
)
".venv\Scripts\python.exe" "etapa_04_claude_api\python\informe_comercial.py" --local
exit /b %errorlevel%
