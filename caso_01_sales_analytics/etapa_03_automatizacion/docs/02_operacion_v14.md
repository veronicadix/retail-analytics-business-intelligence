# V14 — Operación local y planificación

## Estado
- **Confirmado por ejecución del usuario (21/10/2026):** V13 completó `movimientos_stage` y copió a `movimientos_raw`: **1.033.036** registros. No se han ejecutado los cambios V14.
- V14 conserva los trabajos BigQuery compatibles con Sandbox; **no utiliza MERGE**.
- El CSV exportado es temporal. La carga final sobrescribe toda la tabla, no realiza actualización incremental.

## Nuevas capacidades V14
- `logs/pipeline.log`: salida informativa acumulada de cada ejecución; no imprimir secretos.
- `logs/historial_ejecuciones.jsonl`: por ejecución registra ID, modo, inicio/fin UTC, duración, estado y tipo de error si aplica.
- `logs/pipeline.lock`: archivo creado con exclusividad para evitar dos procesos locales ejecutándose a la vez. Se elimina al terminar. Si el proceso se interrumpe bruscamente, verificar que esté inactivo antes de retirar manualmente el bloqueo.
- `ejecutar_pipeline.cmd`: comando preparado para Programador de tareas de Windows.

## Preparación y prueba en CMD
1. Extraer la carpeta `proyecto-ventas-gcp-ai V14` junto a V13.
2. Abrir CMD en V14 y crear entorno propio:
   `python -m venv .venv`
3. Instalar dependencias:
   `.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt`
4. Copiar el `.env` que funcionó desde V13, sin compartirlo ni subirlo al repositorio:
   `copy "..\proyecto-ventas-gcp-ai V13\.env" ".env"`
5. Comprobar sin escribir en las bases:
   `.venv\Scripts\python.exe etapa_03_automatizacion\python\pipeline_retail.py --check`
6. Inspeccionar los archivos `logs/pipeline.log` y `logs/historial_ejecuciones.jsonl`.
7. Ejecutar `--run` **solo cuando se quiera reemplazar la tabla completa**:
   `.venv\Scripts\python.exe etapa_03_automatizacion\python\pipeline_retail.py --run`

## Programación local (opcional, no configurada)
- Abrir **Programador de tareas → Crear tarea**.
- Acción **Iniciar un programa**: indicar la ruta absoluta de `etapa_03_automatizacion\ejecutar_pipeline.cmd`.
- Establecer frecuencia adecuada (por ejemplo semanal) y ejecutar **solo cuando el equipo esté encendido y tenga acceso a PostgreSQL e Internet**.
- El usuario de Windows debe disponer de credenciales ADC y acceso a PostgreSQL.
- No configurar reintentos automáticos de tareas mientras no se revise el historial de errores. Las cargas repetidas son completas y consumen cuotas.

## Seguridad y límites
- `.env`, `.venv`, `logs/`, `data/*.csv`, credenciales y `.pbix` quedan fuera de GitHub.
- Este bloqueo evita duplicación concurrente **solo en la misma carpeta local**, no entre equipos o instancias en nube.
- La copia final de staging a raw puede interrumpirse por permisos o cuotas de Sandbox. En ese caso se registra ERROR y el origen no se modifica.
- Se conservan los controles existentes antes de reemplazar raw (conteo y unicidad en staging).
- Los logs NO constituyen monitoreo remoto ni alertas por correo: queda pendiente.
