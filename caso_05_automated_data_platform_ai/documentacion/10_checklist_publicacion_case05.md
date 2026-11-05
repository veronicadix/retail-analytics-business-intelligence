# Caso 05 — Checklist de publicación segura en GitHub

**Objetivo:** publicar el Caso 05 sin afectar cambios de los casos 01–04 y sin exponer secretos ni artefactos operativos. Estado inicial: pendiente de ejecutar los controles en la copia local.

## 1. Archivos que sí deben publicarse

- [ ] `README.md` (español) y `README_EN.md` (inglés), ambos dentro de `caso_05_automated_data_platform_ai/`.
- [ ] Scripts `python/03_pipeline_postgresql_bigquery.py`, `08_orquestador_case05.py`, `08_validar_metricas.py`, `09_insights_claude.py`.
- [ ] Consultas de `sql/` y los cinco modelos `dbt/models/` con sus YAML.
- [ ] `dbt/dbt_project.yml`.
- [ ] Guías de `documentacion/`.
- [ ] Solo evidencias **agregadas y revisadas** (CSV de calidad, CSV de conciliación, reporte IA Markdown si su texto fue validado). No es necesario publicar los JSON operativos íntegros.

## 2. Archivos que NO deben publicarse

- [ ] `.env`, `.env.*` excepto una plantilla `.env.example` sin secretos.
- [ ] `*.key`, `*.pem`, tokens, JSON de cuentas de servicio, credenciales locales, archivos de autenticación de Google Cloud.
- [ ] `.venv/`, `venv/`, `__pycache__/`, `*.pyc`, `.user.yml` de dbt y carpetas `dbt/target/`, `dbt/logs/`, `dbt/dbt_packages/`.
- [ ] Carpetas `logs/`, ZIP descargados, copias `caso05_modelos_dbt/`, `caso05_etapa06_claude/`, `claude_extraido/` y otros archivos temporales.
- [ ] `resultados/08_orquestacion_*.json` y `resultados/09_insights_claude_*.json` sin revisión, ya que pueden contener textos internos, identificadores y metadatos.
- [ ] `dbt/profiles.yml` antes de comprobar que no tiene información secreta; en este caso podría publicarse como ejemplo saneado, pero no es obligatorio.

## 3. Fragmento recomendado para agregar AL FINAL del `.gitignore` de la raíz

```gitignore
# Caso 05: entornos y archivos operativos
/caso_05_automated_data_platform_ai/.venv/
/caso_05_automated_data_platform_ai/logs/
/caso_05_automated_data_platform_ai/dbt/target/
/caso_05_automated_data_platform_ai/dbt/logs/
/caso_05_automated_data_platform_ai/dbt/dbt_packages/
/caso_05_automated_data_platform_ai/dbt/.user.yml
/caso_05_automated_data_platform_ai/dbt/profiles.yml
/caso_05_automated_data_platform_ai/caso05_modelos_dbt/
/caso_05_automated_data_platform_ai/caso05_etapa06_claude/
/caso_05_automated_data_platform_ai/claude_extraido/
/caso_05_automated_data_platform_ai/*.zip
/caso_05_automated_data_platform_ai/resultados/08_orquestacion_*.json
/caso_05_automated_data_platform_ai/resultados/09_insights_claude_*.json

# Excepciones: publicar SOLO los CSV agregados validados del Caso 05
!/caso_05_automated_data_platform_ai/resultados/04_validacion_calidad_bigquery.csv
!/caso_05_automated_data_platform_ai/resultados/07_conciliacion_metricas_comerciales.csv
```

> El `.gitignore` principal ya incluye `*.csv`, por eso las dos excepciones son necesarias para los resultados agregados. Verifica que los archivos existan antes de agregarlos. `*.json` no está excluido globalmente: la revisión manual sigue siendo esencial.

## 4. Revisiones desde CMD

Desde la raíz del repositorio, ejecutar:

```bat
git status --short
git check-ignore -v caso_05_automated_data_platform_ai\.env
git check-ignore -v caso_05_automated_data_platform_ai\dbt\target\manifest.json
```

Los dos últimos comandos deberían mostrar una regla que ignora esos archivos (el segundo solo si existe `manifest.json`). También se pueden revisar los archivos visualmente en GitHub Desktop. No subas ninguna clave ni la pegues en CMD.

## 5. GitHub Desktop

1. Abrir el repositorio `retail-analytics-business-intelligence`.
2. Revisar *Changes* y seleccionar **solo** el Caso 05 y el `.gitignore` necesario. Dejar sin seleccionar el ZIP y cualquier cambio pendiente del Caso 02 u otros casos.
3. Comprobar que las rutas y archivos son los esperados; revisar el diff para descartar secretos, datos identificables y archivos gigantes.
4. **Summary:** `feat: publish case 05 automated retail pipeline and AI insights`.
5. **Description:** `Add PostgreSQL-to-BigQuery ETL, five dbt models, 14 data tests, six reconciled KPIs, local orchestration, Claude API report and bilingual documentation.`
6. Ejecutar **Commit to main**, luego **Push origin**.
7. Abrir el Caso 05 en GitHub y comprobar README, scripts, modelos, documentación y resultados agregados.

## 6. Evidencias y afirmaciones finales

- [ ] Pipeline: 1.077.856 filas; 3 tablas; diferencias de conteo = 0.
- [ ] dbt: 5 modelos construidos y 14/14 pruebas aprobadas.
- [ ] Métricas: 6/6 con diferencia 0.
- [ ] Orquestador `verify`: al menos una ejecución local `COMPLETADO`.
- [ ] Claude: informe Markdown y JSON generados localmente; revisar el texto y no publicar la API key.
- [ ] Programación semanal de Windows: **configurada**, pero no indicar que se validó en producción hasta comprobar la ejecución automática posterior.
- [ ] Confirmación final de publicación: verificar URL y contenido en GitHub, no inferirla solo por GitHub Desktop.

**Nota de seguridad:** una API Key anterior fue expuesta durante el desarrollo. La clave publicada accidentalmente debe permanecer revocada; utilizar exclusivamente una clave nueva guardada en `.env` local.
