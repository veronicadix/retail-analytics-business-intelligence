# Case 04 | E-commerce Conversion & Business Requirements

**Retail Analytics & Business Intelligence Portfolio** · Business Analysis · SQL · Google BigQuery · GA4 · BPMN · UAT

[Versión en español](README.md)

## Executive summary

A portfolio case study using the public, obfuscated **Google Analytics 4 E-commerce Sample** to examine sequential purchase journeys and translate analytics findings into business requirements, BPMN process models, Agile user stories, acceptance criteria, and a proposed UAT test suite.

**Business question:** At which journey stages do users stop progressing through the observed sequence, and what requirements would help measure and validate potential improvements?

> **Scope:** exploratory analysis and functional solution design. This project does not implement changes to the e-commerce site or claim that acceptance tests have been executed. Potential friction points are hypotheses rather than verified root causes.

## Data and methodology

- **Source:** `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`.
- **Period:** November 1, 2020–January 31, 2021 (92 observed calendar days in the event exploration).
- **Tools:** Google BigQuery SQL, Bizagi Modeler / BPMN 2.0, Markdown, CSV.
- **Funnel unit:** unique non-null `user_pseudo_id` values progressing through events in timestamp order.
- **Main funnel:** `view_item → add_to_cart → begin_checkout → purchase`.
- **Checkout subfunnel:** `begin_checkout → add_shipping_info → add_payment_info → purchase`.

The two funnels have **different starting populations**. Checkout starts from all observed `begin_checkout` users; it is not restricted to users who first passed through `view_item`. The queries do not enforce a single session or product and may exclude valid alternative journeys or journeys with missing events.

## Key results

### Main funnel — query 02

| Event | Users | Step conversion | Did not progress to next stage / step drop-off | Cumulative conversion |
|---|---:|---:|---:|---:|
| `view_item` | 61,252 | — | — | 100.00% |
| `add_to_cart` | 12,052 | 19.68% | 80.32% | 19.68% |
| `begin_checkout` | 4,909 | 40.73% | 59.27% | 8.01% |
| `purchase` | 2,833 | 57.71% | 42.29% | **4.63%** |

The largest decrease occurs between product view and add-to-cart: 49,200 users in the initial population did not complete that sequential stage.

### Checkout subfunnel — query 03

| Event | Users | Step conversion | Step drop-off |
|---|---:|---:|---:|
| `begin_checkout` | 9,715 | — | — |
| `add_shipping_info` | 6,588 | 67.81% | 32.19% |
| `add_payment_info` | 4,334 | 65.79% | 34.21% |
| `purchase` | 3,320 | 76.60% | 23.40% |

**34.17%** of the 9,715 users starting this checkout subfunnel completed its full observed event sequence. The highest proportional step reduction is shipping → payment (**34.21%**), while the greatest absolute reduction is checkout → shipping (**3,127 users**).

### Event-quality observation

In query 01, `add_to_cart` was observed on **74 days**, compared with `purchase` on **92 days**. Event coverage and tagging should be investigated before attributing all observed reductions to user experience.

## Business hypotheses and proposed improvements

1. Investigate product-detail clarity, calls to action, and event instrumentation.
2. Improve shipping-form validation and collect privacy-safe error telemetry.
3. Assess transparency of shipping costs, taxes, and totals before payment.
4. Design payment status, error handling, and safe retry flows that avoid duplicate orders.
5. Monitor event coverage and evaluate UX changes through controlled experiments.

The dataset does **not** directly establish why customers did not proceed, whether payment failures occurred, or whether unexpected fees were shown.

## Project deliverables

| Item | Files |
|---|---|
| Event exploration | [`sql/01_exploracion_eventos_ga4.sql`](sql/01_exploracion_eventos_ga4.sql) · [`resultados/01_exploracion_eventos_ga4.csv`](resultados/01_exploracion_eventos_ga4.csv) |
| Main conversion funnel | [`sql/02_funnel_conversion_ga4.sql`](sql/02_funnel_conversion_ga4.sql) · [`resultados/02_funnel_conversion_ga4.csv`](resultados/02_funnel_conversion_ga4.csv) |
| Checkout subfunnel | [`sql/03_checkout_dropoff_ga4.sql`](sql/03_checkout_dropoff_ga4.sql) · [`resultados/03_checkout_dropoff_ga4.csv`](resultados/03_checkout_dropoff_ga4.csv) |
| Business findings | [`documentacion/04_analisis_hallazgos_comerciales.md`](documentacion/04_analisis_hallazgos_comerciales.md) |
| Business requirements document | [`documentacion/BRD/05_brd_ecommerce_checkout.md`](documentacion/BRD/05_brd_ecommerce_checkout.md) |
| AS-IS / TO-BE BPMN models | [`documentacion/BPMN/06_bpmn_as_is_checkout.bpmn`](documentacion/BPMN/06_bpmn_as_is_checkout.bpmn) · [`documentacion/BPMN/06_bpmn_to_be_checkout.bpmn`](documentacion/BPMN/06_bpmn_to_be_checkout.bpmn) |
| Agile user stories and acceptance criteria | [`documentacion/historias_usuario/07_historias_usuario_criterios_aceptacion.md`](documentacion/historias_usuario/07_historias_usuario_criterios_aceptacion.md) |
| UAT test matrix | [`documentacion/UAT/08_matriz_pruebas_uat.csv`](documentacion/UAT/08_matriz_pruebas_uat.csv) · [`documentacion/UAT/08_matriz_pruebas_uat.md`](documentacion/UAT/08_matriz_pruebas_uat.md) |

Import `.bpmn` files in Bizagi Modeler using **Import → BPMN**. Exported process images may be stored in `visualizaciones/`.

## Traceability and testing status

**GA4 data → SQL queries and CSV results → business findings → requirements (RN/RF) → user stories HU-01–HU-10 → 31 UAT scenarios.**

All **31 UAT scenarios are designed but not executed**. No acceptance approval, feature deployment, or realized conversion uplift is claimed.

## Reproduce the analysis

1. Open Google BigQuery with access to `bigquery-public-data`; use processing location **US** for the public dataset.
2. Run the numbered `.sql` files in `sql/` and compare the outputs with the matching CSV files in `resultados/`.
3. Preserve the date range and event-order conditions when comparing rates.
4. Read the BRD, user stories, and UAT matrix as **proposed design artifacts**, not evidence of a shipped implementation.
5. Never publish credentials, access tokens, or personal data in this repository.

## Skills demonstrated

BigQuery SQL · GA4 event analytics · funnel analysis · data quality · business requirements · BPMN process modeling · Agile user stories · acceptance criteria · UAT test design · functional traceability.

**Source:** [Google Analytics sample dataset for BigQuery (official documentation)](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset).
