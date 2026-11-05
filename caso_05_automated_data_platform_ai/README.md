# Caso 05 — Plataforma automatizada de datos retail e insights con IA

**Portafolio Retail Analytics & Business Intelligence** · Python · PostgreSQL · Google BigQuery · dbt · Claude API · Windows Task Scheduler

> **Estado:** pipeline y modelos ejecutados y validados; programación semanal configurada (primera ejecución automática aún pendiente de comprobar). Proyecto de portafolio con datos históricos de e-commerce; no es un sistema productivo.

[English version](README_EN.md)

## Resumen ejecutivo

Este caso implementa una cadena de datos comerciales desde PostgreSQL hasta Google BigQuery, transforma los datos mediante modelos dbt, incorpora controles de calidad y conciliación, ejecuta validaciones mediante un orquestador Python y genera un informe ejecutivo asistido por Claude API. La IA **no calcula los indicadores financieros**: recibe métricas agregadas previamente conciliadas y produce una interpretación sujeta a revisión humana.

### Resultados comprobados

| Indicador | Resultado |
|---|---:|
| Registros cargados y conciliados PostgreSQL → BigQuery | **1.077.856** |
| `base_movimientos` | 1.033.036 |
| `catalogo_codigos` | 5.304 |
| `facturas_venta` | 39.516 |
| Modelos dbt ejecutados | **5/5** |
| Pruebas dbt aprobadas | **14/14** |
| Indicadores comerciales conciliados | **6/6**, diferencia 0 |
| Orquestación local `verify` | Ejecutada correctamente |
| Informe Claude API | Generado (240 tokens entrada, 482 salida en la ejecución reportada) |

La conciliación de conteos no equivale a una comprobación campo por campo. Los controles de integridad cubren los atributos y las reglas documentadas, no toda posible anomalía.

## Arquitectura

```text
PostgreSQL: portafolio_retail
   ├── base_movimientos
   ├── catalogo_codigos
   └── facturas_venta
         │
         ▼
Python ETL (carga por lotes + validación)
         │
         ▼
BigQuery / retail_pipeline_case05  [fuentes]
         │
         ▼
dbt / retail_case05_dbt        [5 vistas]
         │
         ├── 14 tests de calidad
         ├── conciliación de 6 métricas
         └── orquestador local (modo verify / full)
                      │
                      ▼
              resultados y logs locales
                      │
                      ▼
              Claude API (resumen de métricas validadas)
                      │
                      ▼
              Informe Markdown + evidencia JSON
```

El `verify` **no recarga datos de PostgreSQL**: ejecuta las transformaciones dbt, sus pruebas y la conciliación comercial. El modo `full` puede volver a cargar tablas y debe utilizarse conscientemente. La tarea de Windows `Caso05_Verify_Semanal` está configurada los **viernes a las 09:00, hora local de Bogotá**, en modo interactivo; requiere una sesión iniciada. Su primera ejecución automática todavía no ha sido verificada.

## Indicadores comerciales conciliados

| Métrica | Fuente y mart dbt | Diferencia |
|---|---:|---:|
| Ventas brutas | GBP 19.643.861,637 | 0 |
| Abonos de mercancía | GBP −716.462,57 | 0 |
| Ventas netas | GBP 18.927.399,067 | 0 |
| Unidades de demanda | 11.188.061 | 0 |
| Líneas totales | 1.033.036 | 0 |
| Líneas de venta | 1.003.357 | 0 |

Periodo histórico del origen: **2009-12-01 07:45:00 a 2011-12-09 12:50:00**. La fuente de verdad de estas cifras es la conciliación SQL del Caso 05; las recomendaciones de IA no se consideran resultados implementados.

## Estructura del proyecto

```text
caso_05_automated_data_platform_ai/
├── python/
│   ├── 03_pipeline_postgresql_bigquery.py
│   ├── 08_orquestador_case05.py
│   ├── 08_validar_metricas.py
│   └── 09_insights_claude.py
├── sql/
│   ├── 01_inventario_origen_postgresql.sql
│   ├── 02_volumen_y_cobertura_origen.sql
│   ├── 04_validacion_calidad_bigquery.sql
│   └── 07_conciliacion_metricas_comerciales.sql
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml                 # revisar antes de publicar
│   └── models/
│       ├── schema.yml
│       ├── staging/
│       └── marts/
├── documentacion/
│   ├── 03_instrucciones_ejecucion.md
│   ├── 08_guia_orquestacion_local.md
│   └── 09_guia_integracion_claude.md
├── resultados/                      # publicar solo evidencias revisadas
├── README.md
└── README_EN.md
```

Los archivos generados por distintas ejecuciones pueden variar de nombre. Las carpetas `.venv`, `dbt/target`, `dbt/logs`, `logs`, `.env` y claves **no** forman parte del entregable público.

## Reproducibilidad (resumen)

**Requisitos:** PostgreSQL y base `portafolio_retail` preparados; acceso a BigQuery; Python y dependencias indicadas en el proyecto; dbt Core y adaptador dbt-bigquery; Git; permisos adecuados en Google Cloud. Las versiones verificadas durante el desarrollo incluyeron `psycopg 3.3.7`, `dbt-bigquery 1.12.1` y SDK Anthropic `2.4.0`; comprobar y fijar versiones del entorno reproducible antes de una nueva instalación. La ejecución dbt reportó Core `1.13.0-b1` (beta), aspecto por estabilizar en la siguiente iteración.

1. Crear un `.env` local a partir de una plantilla sin secretos y configurar las variables de conexión requeridas. **Nunca subir `.env`.**
2. Configurar Application Default Credentials de Google Cloud y verificar el proyecto `maximal-arcade-512100-h2` y la ubicación `US`.
3. Ejecución inicial controlada: `python python/03_pipeline_postgresql_bigquery.py` desde el entorno Python del pipeline.
4. Desde `dbt/`, ejecutar `dbt run --profiles-dir .` y `dbt test --profiles-dir .` usando el ejecutable de dbt instalado.
5. Ejecutar la consulta `sql/07_conciliacion_metricas_comerciales.sql` (ubicación de procesamiento `US`).
6. Desde la raíz del caso, ejecutar `python python/08_orquestador_case05.py --mode verify` en el entorno del pipeline.
7. Instalar el SDK de Anthropic en un entorno separado, configurar `ANTHROPIC_API_KEY` localmente, probar `python python/09_insights_claude.py` sin consumir créditos y después usar `--live` solo cuando se quiera emitir una solicitud de pago.

Estas instrucciones describen la secuencia; las rutas y los comandos exactos de Windows están detallados en `documentacion/`. Para replicar el proyecto en otra cuenta, actualizar el ID de proyecto y las referencias SQL, y crear los datasets en una ubicación compatible.

## Calidad, limitaciones y seguridad

- Las 14 pruebas dbt pasaron y los 6 indicadores presentaron diferencia cero en la ejecución reportada; no afirmamos que se haya realizado una auditoría exhaustiva de todas las filas.
- El orquestador fue verificado localmente. El uso semanal mediante el Programador de tareas está **configurado pero aún no validado con una ejecución automática real**.
- PostgreSQL se ejecuta en `localhost`; GitHub-hosted Actions no puede conectarse directamente a ese servicio sin infraestructura adicional. No se declara CI/CD remoto implementado.
- El reporte de Claude es **asistido por IA** y debe revisarse antes de publicarse. El consumo de 240 tokens de entrada y 482 de salida se registró en la ejecución del 5 de noviembre de 2026.
- No publicar claves, `.env`, datos privados, trazas con información sensible ni archivos de credenciales. Revisar los CSV/JSON agregados antes de incluirlos en Git.

## Próximas mejoras

Fijar dependencias y eliminar la versión beta de dbt, ejecutar y comprobar la primera tarea programada, incorporar pruebas más profundas de integridad referencial y conciliación, y evaluar una orquestación en la nube con conectividad segura a la fuente.

**Naturaleza del proyecto:** ejercicio personal de portafolio; los datos y los informes son históricos y no reflejan operaciones comerciales en tiempo real.
