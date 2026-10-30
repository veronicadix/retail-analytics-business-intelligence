# V15 — Programacion local del pipeline

## Estado de referencia
- V13: carga completa ejecutada con exito en BigQuery Sandbox, 1.033.036 registros.
- V14: `--check` exitoso, logs y `historial_ejecuciones.jsonl` confirmados.
- V15: prepara una tarea **semanal los lunes a las 08:00** (hora local configurada en Windows; Bogota prevista).
- Esta entrega **no instala ni ejecuta** ninguna tarea en el equipo automaticamente.

## Alcance
- Ejecuta `pipeline_retail.py --run` desde Python del `.venv` propio de V15.
- Usa ADC del usuario Windows y `.env` local; nunca utiliza cuentas SYSTEM ni contrasenas en comandos.
- El pipeline conserva el bloqueo `pipeline.lock`, logs y reemplazo completo de raw tras validar staging.
- Si el usuario no ha iniciado sesion, la tarea interactiva **no corre**; si el equipo esta apagado tampoco. `StartWhenAvailable` puede intentar recuperar una ejecucion omitida cuando vuelva a estar disponible una sesion, no garantiza todas.
- **Aviso:** las tablas de origen de PostgreSQL deben estar accesibles; se requiere Internet y credenciales ADC vigentes.

## Preparacion en CMD — una sola vez
Abrir CMD normal (no como administrador) e introducir un comando por vez:

```cmd
cd /d "C:\ruta\a\Portafolio_Data_Engineering\proyecto-ventas-gcp-ai V15"
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt
copy "..\proyecto-ventas-gcp-ai V14\.env" ".env"
.venv\Scripts\python.exe etapa_03_automatizacion\python\pipeline_retail.py --check
```

Se debe verificar `CHECK correcto` y `estado=OK` antes de programar. No copiar `.env` si el anterior contiene datos distintos de los vigentes; editarlo localmente. Nunca pegar su contenido en chats o GitHub.

## Registrar tarea desde CMD (no realiza carga)

```cmd
powershell -NoProfile -ExecutionPolicy Bypass -File "etapa_03_automatizacion\programacion\instalar_tarea.ps1"
schtasks /Query /TN "Retail_Pipeline_Semanal" /V /FO LIST
```

Si Windows informa que la tarea ya existe, **no la sobreescriba** sin revisarla. Para modificar el dia, editar `-DaysOfWeek Monday` en `instalar_tarea.ps1` ANTES de crear la tarea.

## Operacion (CMD)

```cmd
schtasks /Query /TN "Retail_Pipeline_Semanal" /V /FO LIST
schtasks /Change /TN "Retail_Pipeline_Semanal" /Disable
schtasks /Change /TN "Retail_Pipeline_Semanal" /Enable
```

El comando de prueba `schtasks /Run /TN "Retail_Pipeline_Semanal"` **SI ejecuta carga real**; no usar hasta que sea necesario. Para retirar la tarea:

```cmd
schtasks /Delete /TN "Retail_Pipeline_Semanal" /F
```

Consultar resultados sin ejecutar:

```cmd
type etapa_03_automatizacion\logs\historial_ejecuciones.jsonl
type etapa_03_automatizacion\logs\pipeline.log
```

## Criterios de aceptacion
1. Registrar la tarea en Windows (confirmacion en `schtasks /Query`).
2. Validar que existe una proxima ejecucion programada el lunes a las 08:00, hora local.
3. Verificar historial tras el primer lunes ejecutado: `estado: OK`, `modo: --run`, y conteo final correspondiente.
4. Si falla, revisar ultimo resultado de la tarea, `pipeline.log` y presencia de `pipeline.lock`; no eliminar el bloqueo hasta comprobar que no exista un proceso activo.

## Riesgos y limites
- BigQuery Sandbox: reemplazo completo con jobs de carga/copia, **no** MERGE.
- La primera ejecucion programada aun no ha sido comprobada.
- No se programan Cloud Run, Cloud Scheduler ni Claude API en V15.
- No subir `.env`, `.venv`, `.pbix`, CSV ni logs al repositorio GitHub.
- Mantener el computador encendido con sesion Windows iniciada y PostgreSQL local operativo.
