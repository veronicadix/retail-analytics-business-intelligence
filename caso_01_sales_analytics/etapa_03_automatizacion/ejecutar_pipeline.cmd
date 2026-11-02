@echo off
REM Ejecutar desde Programador de tareas o con doble clic.
REM Se ubica en la raíz del proyecto independientemente del directorio actual.
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Falta el entorno virtual .venv en esta version.
  exit /b 2
)
".venv\Scripts\python.exe" "etapa_03_automatizacion\python\pipeline_retail.py" --run
exit /b %errorlevel%
