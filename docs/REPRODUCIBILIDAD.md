# Reproducibilidad y ejecución local

## Requisitos

- Python y paquetes instalados mediante `requirements.txt` de las etapas correspondientes.
- PostgreSQL configurado localmente y datos de origen disponibles.
- Google Cloud CLI y credenciales de aplicación (`gcloud auth application-default login`), con permisos sobre BigQuery.
- Power BI Desktop para abrir y editar el dashboard local (no distribuido públicamente).

## Orden y comandos de referencia

Desde la raíz local del proyecto, instalar dependencias en un entorno `.venv` nuevo:

```cmd
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt
.venv\Scripts\python.exe -m pip install -r etapa_04_claude_api\requirements.txt
```

1. Revisar los SQL de etapa 01/02 antes de aplicar sobre bases nuevas.
2. Usar el pipeline con `--check` para comprobar conexiones; `--run` reemplaza la tabla de destino y **no debe ejecutarse sobre datos ajenos sin revisión**.
3. Ejecutar el informe local `etapa_04_claude_api/python/informe_comercial.py --local`, sin Claude API.
4. Ejecutar el motor de reglas `etapa_05_inteligencia_comercial/python/motor_comercial.py --local`.
5. Convertir el JSON local resultante en CSV mediante `etapa_06_powerbi_portafolio/python/exportar_powerbi.py --from-json RUTA_AL_JSON`.
6. Importar los CSV en Power BI Desktop, revisar localización `en-US` para campos decimales y usar DAX documentado.

**No ejecutar pasos destructivos ni programar automáticamente el proceso sin revisar primero los archivos `.cmd` y `.ps1` contra las rutas de tu equipo.** El repositorio público no incluye el entorno de datos ni el `.pbix`.
