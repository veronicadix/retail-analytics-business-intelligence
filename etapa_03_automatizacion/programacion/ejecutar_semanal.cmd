@echo off
REM V15 - Ejecutable utilizado por el Programador de tareas de Windows.
REM Determinar la raiz del proyecto independientemente del directorio activo.
setlocal
cd /d "%~dp0..\.." || exit /b 10
REM Utilizar Python del entorno virtual de ESTA version, sin activacion.
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: falta .venv en V15. Consulte la guia de instalacion.
  exit /b 11
)
REM --run: genera CSV temporal, valida staging y reemplaza raw en Sandbox.
REM La salida persistente se registra en logs por pipeline_retail.py.
".venv\Scripts\python.exe" "etapa_03_automatizacion\python\pipeline_retail.py" --run
set "RC=%ERRORLEVEL%"
exit /b %RC%
