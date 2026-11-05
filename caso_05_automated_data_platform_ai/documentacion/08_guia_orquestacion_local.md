# Caso 05 — Entregable 08: orquestación local y controles operativos

## Alcance

El pipeline PostgreSQL → BigQuery y los cinco modelos dbt ya fueron ejecutados con éxito. Esta entrega **no es un programador automático todavía**; prepara una ejecución unificada y registrable en Windows. No requiere GitHub Actions ni publicar el servidor PostgreSQL en Internet.

**Modos disponibles:**

- `--mode verify` (predeterminado): `dbt run` → `dbt test` → conciliación de 6 métricas. `dbt run` **sí actualiza/recrea las vistas** del dataset de modelos `retail_case05_dbt`; no ejecuta el ETL ni reemplaza las tablas de origen de `retail_pipeline_case05`.
- `--mode full`: ejecuta primero `03_pipeline_postgresql_bigquery.py` y verifica su JSON de conciliación (3 tablas, 1.077.856 registros de referencia), después ejecuta los mismos pasos dbt. **El ETL usa WRITE_TRUNCATE sobre las tablas finales del Caso 05**, después de verificar la carga temporal. No ejecutar mientras existan cargas externas ni si cambió el conjunto histórico sin revisar el control de cantidades.

**Reintentos:** solo la consulta de lectura de las 6 métricas admite un reintento (dos intentos totales). No reintenta automáticamente el ETL ni `dbt run` porque realizan escrituras. Si una etapa falla, las siguientes **no se ejecutan** y queda un reporte de error. El ETL tiene promoción por tabla, no una transacción global sobre las tres.

## Instalación — copiar estos archivos

Desde este ZIP a la carpeta principal:

```
caso_05_automated_data_platform_ai/
├── python/
│   ├── 03_pipeline_postgresql_bigquery.py   # existente; conservar
│   ├── 08_orquestador_case05.py             # nuevo
│   └── 08_validar_metricas.py              # nuevo
├── sql/
│   └── 07_conciliacion_metricas_comerciales.sql  # ya existente, no sobrescribir
├── documentacion/
│   └── 08_guia_orquestacion_local.md
├── .venv/                               # existente, local y excluido del repositorio
├── dbt/                                # existente
├── resultados/                          # salidas JSON
└── logs/                                # nuevos logs locales, excluidos de Git
```

Solo necesitas copiar los dos scripts nuevos a `python/` y la guía a `documentacion/`. El SQL se incluye únicamente como referencia; **si ya lo tienes en `sql/`, consérvalo sin reemplazarlo**.

## Comandos de CMD en Windows

```bat
cd /d "C:\Users\HEWLETT PACKARD\OneDrive\Documentos\Portafolio_Data_Engineering\retail-analytics-business-intelligence\caso_05_automated_data_platform_ai"
.venv\Scripts\python.exe python\08_orquestador_case05.py --mode verify
```

Solamente cuando necesites repetir la carga completa de PostgreSQL:

```bat
.venv\Scripts\python.exe python\08_orquestador_case05.py --mode full
```

El orquestador utiliza `C:\venvs\retail05_dbt\Scripts\dbt.exe` para dbt y la `.venv` propia del Caso 05 para la conciliación de BigQuery; ambas ubicaciones provienen de la configuración que ya verificamos. Si cambian:

```bat
.venv\Scripts\python.exe python\08_orquestador_case05.py --mode verify --dbt-exe "C:\ruta\dbt.exe" --python-etl "C:\ruta\python.exe"
```

## Salidas por ejecución

- `logs/08_orquestacion_<id>.log`: registro de etapas y salidas de procesos.
- `resultados/08_orquestacion_<id>.json`: resumen de pasos, estado final, hora UTC y ruta del log.
- `resultados/03_conciliacion_postgresql_bigquery.json`: se actualiza solamente en modo `full` después del ETL.

El JSON final puede tener `estado: OK` o `estado: ERROR`. Nunca interpretar el estado OK como prueba de identidad fila por fila: los controles actuales son conteos, pruebas dbt y seis métricas.

## Condiciones previas

1. PostgreSQL y las credenciales `.env` solo son necesarios para `full`.
2. dbt debe conectarse a `maximal-arcade-512100-h2`, región `US`, y reconocer sus cinco modelos.
3. El SQL `sql/07_conciliacion_metricas_comerciales.sql` debe existir y las tablas de origen y marts deben ser accesibles.
4. Deben estar instalados `google-cloud-bigquery` en `.venv` y dbt en `C:\venvs\retail05_dbt`.
5. El script de carga original debe conservar la corrección `LOCATION = 'US'` y una comparación insensible a mayúsculas en `ds.location`.

## Seguridad y Git

No subir `.env`, credenciales de Google, archivos de credenciales ADC, `.venv`, `dbt/target`, `dbt/logs`, `logs` ni `dbt/.user.yml`. Añade al `.gitignore` del repositorio, si no existen:

```gitignore
/caso_05_automated_data_platform_ai/logs/
/caso_05_automated_data_platform_ai/dbt/logs/
/caso_05_automated_data_platform_ai/dbt/target/
/caso_05_automated_data_platform_ai/dbt/.user.yml
```

No activar GitHub Actions como mecanismo de ETL de PostgreSQL: los runners hospedados en GitHub no alcanzan `localhost` de tu PC. Una tarea programada de Windows o un runner *self-hosted* serían alternativas futuras con el equipo encendido y controles de acceso adecuados; **no están configuradas en esta entrega**.

## Evidencia para el portafolio

Ejecuta `verify` una vez y comparte las últimas líneas del CMD junto con el estado y pasos del JSON (sin credenciales). Si hay errores, conserva el log local, pero evita publicarlo completo sin revisar datos sensibles. El siguiente entregable será automatización programada y/o alertas, una vez validado este orquestador.
