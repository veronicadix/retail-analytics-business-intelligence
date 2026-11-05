# Caso 05 — Etapa 02: Pipeline PostgreSQL → BigQuery

## Alcance

Carga `public.base_movimientos`, `public.catalogo_codigos` y `public.facturas_venta` de PostgreSQL a `retail_pipeline_case05` (región `us-central1`) del proyecto GCP configurado en `.env`. Los datos se exportan temporalmente a JSONL en el equipo (sin subir a GitHub), se cargan en tablas temporales de BigQuery, se validan por conteo y unicidad y finalmente se copian a tablas del dataset del caso. **Las tablas de los casos anteriores no se tocan.**

La promoción es **por tabla**, no atómica entre las tres: si falla una tabla posterior, las anteriores pueden haber sido actualizadas. Reejecutar sustituye las tres tablas de destino del Caso 05 con el estado actual de origen. No es una carga incremental.

## Instalación en Windows (CMD)

Desde la carpeta raíz `caso_05_automated_data_platform_ai`:

```bat
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
notepad .env
```

Rellenar `PG_PASSWORD` y `GCP_PROJECT_ID` en `.env`. Si la contraseña contiene `#` o espacios, escribirla entre comillas dobles. No compartir `.env` ni cargarlo a GitHub.

Autenticarse con credenciales de aplicación de Google Cloud (Cloud SDK instalado):

```bat
gcloud auth application-default login
```

El usuario de Google debe tener permisos para **crear datasets/tablas**, **cargar datos**, **ejecutar consultas** y **copiar tablas** en el proyecto. Si el dataset ya existe, debe estar en `us-central1`.

Ejecutar:

```bat
.venv\Scripts\python.exe python\03_pipeline_postgresql_bigquery.py
```

**Resultado esperado:** tres líneas `OK`, un archivo `resultados/03_conciliacion_postgresql_bigquery.json` y tablas en BigQuery: `retail_pipeline_case05.base_movimientos`, `.catalogo_codigos`, `.facturas_venta`.

## Seguridad y costes

- `.env` y `.venv/` están excluidos por `.gitignore` del repositorio; comprobar antes de hacer commit.
- El script usa archivos temporales JSONL y los elimina al cerrar cada carga.
- No subir las tablas fuente, archivos temporales ni datos personales del dataset a GitHub.
- BigQuery puede facturar almacenamiento, procesamiento de consultas y cargas según las cuotas de la cuenta. Confirma el proyecto activo antes de ejecutar.
- El mapeo de `numeric` a `NUMERIC` exige valores dentro de la precisión de BigQuery; si alguno no cabe, la carga falla antes de promover la tabla.

## Límites y pendientes

- La comparación actual valida conteos y claves únicas, **no igualdad de todas las columnas**; se puede ampliar con checksums por columna o agregados de negocio en la siguiente etapa.
- Se usan transacciones de lectura de PostgreSQL por tabla, no una instantánea global de las tres.
- `COUNT(DISTINCT ...)` y conteos de destino pueden generar procesamiento facturable.
- El script no configura cron, GitHub Actions, Cloud Run ni Claude API: son etapas futuras.
