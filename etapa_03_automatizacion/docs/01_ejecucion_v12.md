# V12 — Primer pipeline local (no programado)

## Estado confirmado
- BigQuery ADC configuradas y Python pudo leer `movimientos_raw`.
- Conteo remoto confirmado: **1.033.036**.
- Proyecto: `retail-data-engineering-512100`; dataset: `retail_analytics`.
- No se ha ejecutado aún el script nuevo, ni se ha validado la conexión Python → PostgreSQL.

## Ejecución
1. Copiar `.env.example` como `.env` **en la raíz de V12**; poner la contraseña local de PostgreSQL en `PGPASSWORD`. No compartirlo.
2. En CMD:
   `cd /d "C:\ruta\a\Portafolio_Data_Engineering\proyecto-ventas-gcp-ai V12"`
3. Crear entorno virtual propio de V12: `python -m venv .venv`
4. Instalar: `.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt`
5. Comprobar sin modificar recursos:
   `.venv\Scripts\python.exe etapa_03_automatizacion\python\pipeline_retail.py --check`
6. Solo después de revisar `--check` y confirmar permisos/cuotas, usar `--run`.

## Comportamiento
- Exportación con COPY del servidor PostgreSQL a archivo temporal local, solo 13 columnas comerciales.
- Carga BigQuery en `movimientos_stage` con reemplazo de tabla de staging.
- Validación de conteos, duplicados y claves antes de ejecutar MERGE.
- MERGE en `movimientos_raw` por `id_linea`: actualiza filas existentes e inserta nuevas, sin duplicarlas.
- Logs a consola, sin imprimir contraseñas.
- Reintentos limitados para fallos temporales al acceder a metadatos y cargar staging; no se repite el MERGE automáticamente.
- El script **no borra registros antiguos** que ya estén en raw pero no aparezcan en la fuente. La actualización es tipo upsert.
- **Sandbox:** algunas operaciones o cuotas pueden estar limitadas. Revisar errores antes de activar Cloud Run o Scheduler.
- Operación programada, alertas y observabilidad en nube: **aún no implementadas**.

## Seguridad y GitHub
- No publicar `.env`, archivos CSV, credenciales ADC, logs ni PBIX.
- No agregar `.venv` al repositorio.
- Verificar que se cuenta con autorización para transferir esos datos a la nube, incluso sin `cliente_id`; `factura` e `id_linea` podrían permitir correlación y se deben tratar como identificadores internos.
