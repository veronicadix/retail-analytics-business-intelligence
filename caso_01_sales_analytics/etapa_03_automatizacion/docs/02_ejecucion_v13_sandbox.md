# V13 — Pipeline compatible con BigQuery Sandbox

## Motivo del cambio
La primera ejecución V12 generó correctamente el CSV (92.808.197 bytes), cargó `movimientos_stage` y superó la comprobación de filas y claves. `MERGE` falló con error **403: DML no admitido sin facturación**. No se actualizó `movimientos_raw` en esa ejecución.

## Implementación V13
1. `COPY` de PostgreSQL a CSV temporal con 13 campos no personales seleccionados.
2. Carga del CSV a `movimientos_stage` mediante `WRITE_TRUNCATE`.
3. Verificación de total de filas, `id_linea` única y no nula; rechazo ante discrepancias.
4. Verificación de unicidad en la tabla final.
5. **Copy job** de staging a `movimientos_raw` con `WRITE_TRUNCATE` (operación atómica).
6. Verificación del total en tabla final y logs de operaciones.

Esta es una **recarga completa** y no un `MERGE` incremental. Si la fuente elimina registros, la tabla final reflejará la fuente completa. No ejecute dos instancias simultáneas. El código no está probado en su entorno: confirmar primero un `--check`, luego un `--run`.

## Comandos CMD en V13
```cmd
cd /d "C:\ruta\a\Portafolio_Data_Engineering\proyecto-ventas-gcp-ai V13"
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt
copy .env.example .env
notepad .env
.venv\Scripts\python.exe etapa_03_automatizacion\python\pipeline_retail.py --check
.venv\Scripts\python.exe etapa_03_automatizacion\python\pipeline_retail.py --run
```

Editar `.env` para introducir la contraseña local, sin compartirla. La cuenta de Google ya utiliza credenciales ADC fuera del proyecto. No subir `.env`, `.venv`, CSV ni PBIX a GitHub.

## Pendientes reales
- Primera prueba del `copy_table` en BigQuery Sandbox.
- Una vez aprobada, registro de ejecuciones en archivo y estrategia de scheduling (Sandbox no incluye Cloud Scheduler gratuito garantizado).
- Control de concurrencia antes de programar ejecuciones.
