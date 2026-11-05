# Case 05 — Automated Retail Data Platform & AI Insights

**Retail Analytics & Business Intelligence Portfolio** · Python · PostgreSQL · Google BigQuery · dbt · Claude API · Windows Task Scheduler

> **Status:** data pipeline and dbt models successfully executed and validated; weekly Windows task configured, but its first scheduled run has not yet been independently verified. This is a portfolio implementation using historical e-commerce data, not a production service.

[Versión en español](README.md)

## Executive summary

This project builds a retail analytics pipeline from PostgreSQL to Google BigQuery, models the data using dbt, validates quality and commercial metrics, coordinates checks with a Python orchestrator, and generates an AI-assisted executive report using Claude API. **Claude does not calculate financial KPIs**; it receives prevalidated, aggregated figures and produces interpretations that require human review.

## Verified outcomes

| Metric | Verified result |
|---|---:|
| PostgreSQL → BigQuery rows transferred and reconciled | **1,077,856** |
| `base_movimientos` | 1,033,036 |
| `catalogo_codigos` | 5,304 |
| `facturas_venta` | 39,516 |
| dbt models built | **5/5** |
| dbt tests passed | **14/14** |
| Business metrics reconciled | **6/6**, zero variance |
| Local orchestrator | Successfully executed in `verify` mode |
| Claude API report | Created (240 input tokens; 482 output tokens in the reported run) |

Row-count reconciliation does not establish row-level or field-level identity for every record; test coverage is limited to the documented controls.

## Architecture

```text
PostgreSQL / portafolio_retail
    (base_movimientos, catalogo_codigos, facturas_venta)
            ↓
Python ETL / batch ingestion and validation
            ↓
BigQuery / retail_pipeline_case05 (source tables)
            ↓
dbt / retail_case05_dbt (five analytical views)
            ↓
14 automated dbt tests + 6 KPI reconciliation checks
            ↓
Python orchestrator / local verification and execution logs
            ↓
Claude API / AI-assisted summary based on validated aggregates
            ↓
Executive Markdown report + structured JSON evidence
```

**Orchestration:** `verify` rebuilds dbt views, runs tests and checks six business measures, without reloading PostgreSQL. `full` may reload source tables and should be invoked explicitly. The Windows task `Caso05_Verify_Semanal` is configured for Fridays at **09:00 Bogotá local time**, using an interactive signed-in Windows session. Its first scheduled run is not yet verified.

## Reconciled business KPIs

| KPI | Source and dbt mart result | Variance |
|---|---:|---:|
| Gross sales | GBP 19,643,861.637 | 0 |
| Merchandise credits | GBP −716,462.57 | 0 |
| Net sales | GBP 18,927,399.067 | 0 |
| Demand units | 11,188,061 | 0 |
| Total transaction lines | 1,033,036 | 0 |
| Sales lines | 1,003,357 | 0 |

Source date range: **December 1, 2009, 07:45:00 to December 9, 2011, 12:50:00**. Claims are grounded in the verified SQL reconciliations rather than model-generated estimates.

## Repository layout

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
│   ├── profiles.yml                 # security-review before publishing
│   └── models/
│       ├── schema.yml
│       ├── staging/
│       └── marts/
├── documentacion/
├── resultados/                      # publish reviewed summaries only
├── README.md
└── README_EN.md
```

Local `.env`, virtual environments, dbt build artifacts, operational logs and credentials must not be committed.

## Reproduction outline

**Prerequisites:** prepared PostgreSQL `portafolio_retail` database; BigQuery access; Python with project dependencies; dbt Core and dbt-bigquery; Git and Google Cloud ADC authentication. Versions observed in the development environment include `psycopg 3.3.7`, `dbt-bigquery 1.12.1` and `anthropic 2.4.0`. dbt Core was reported as `1.13.0-b1` (beta), to be pinned to a stable compatible version in a later iteration.

1. Set up a local `.env` with database and cloud configuration; never commit secrets.
2. Ensure BigQuery project `maximal-arcade-512100-h2` and dataset location `US` are correctly configured.
3. Run the ETL script `python/03_pipeline_postgresql_bigquery.py` in the pipeline Python environment when a refresh is explicitly required.
4. From `dbt/`, run `dbt run --profiles-dir .` followed by `dbt test --profiles-dir .` using the installed dbt executable.
5. Run `sql/07_conciliacion_metricas_comerciales.sql` in the `US` location and verify that all six checks return `OK` and zero variance.
6. Run `python/08_orquestador_case05.py --mode verify` in the pipeline environment for an integrated local check.
7. Configure `ANTHROPIC_API_KEY` in a private `.env`. Run `python/09_insights_claude.py` for a zero-cost dry run, then use `--live` only when an actual billable API request is intended.

For execution details and environment-specific paths, consult the files under `documentacion/`. For other Google Cloud accounts, update project IDs and SQL references and provision compatible datasets.

## Limitations and security

- The recorded run passed 14 dbt tests and reconciled six KPIs, but was **not** a comprehensive row-by-row audit.
- The Windows schedule is configured but its **first autonomous execution remains unverified**.
- PostgreSQL runs on `localhost`; GitHub-hosted runners cannot directly access it without additional infrastructure. Remote CI/CD is **not** presented as implemented.
- Claude-generated findings are hypotheses and recommendations requiring human assessment; the report is not evidence of implemented business improvements.
- Never publish `.env`, API keys, service account files, virtual environments, personal data, sensitive traces or unchecked JSON outputs.

## Potential next steps

Pin all dependencies to a stable set, validate a real scheduled Windows run, expand referential-integrity and financial reconciliation checks, and assess cloud orchestration with secure connectivity.

**Project disclaimer:** personal portfolio work based on historical data; it does not represent real-time business activity.
