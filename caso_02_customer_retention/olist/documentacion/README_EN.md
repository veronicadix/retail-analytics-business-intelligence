# Olist Brazil — Customer Retention & Revenue Growth

**Case 2 | Customer Retention & Revenue Growth**  
**Project:** Retail Analytics & Business Intelligence  
**Tools:** PostgreSQL, SQL, cohort analysis, RFM, and business segmentation.

## Business objective

Analyze purchase frequency and customer retention using Olist's historical Brazilian e-commerce dataset. The goal is to identify second-purchase opportunities and formulate testable commercial hypotheses. This analysis is **independent** of the Online Retail II dataset in the same case: transactions and customer identifiers are not merged across sources.

## Data source and scope

Public source: [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Raw PostgreSQL tables in the `olist` schema:

| Table | Imported rows | Purpose |
|---|---:|---|
| `olist.customers` | 99,441 | Buyer identity via `customer_unique_id` |
| `olist.orders` | 99,441 | Order status and purchase dates |
| `olist.order_items` | 112,650 | Product and freight amounts per line item |

**Analytical population:** orders marked `delivered` with a non-null purchase date and buyer identifier. Order items are first aggregated by `order_id` to avoid inflating order counts. Monetary figures are in **Brazilian reais (BRL)**; product sales exclude freight.

**Analytical purchase-date range:** September 15, 2016–August 29, 2018.

## Key performance indicators

| KPI | Value |
|---|---:|
| Delivered orders analyzed | 96,478 |
| Unique buyers | 93,358 |
| Historical product sales, excluding freight | R$13,221,498.11 |
| Average order product value | R$137.04 |
| One-time buyers | 90,557 |
| Repeat buyers (two or more orders) | 2,801 |
| **Observed repeat purchase rate** | **3.00%** |

**Repeat purchase definition:** buyers with at least two distinct delivered orders divided by all unique buyers with delivered orders during the observation window. It is not a forecast of future purchases.

### Monthly cohort retention

A buyer's cohort is their first delivered-purchase month. A buyer is retained in month *M+n* when they place at least one delivered order in that relative calendar month. Month 0 is 100% by definition. Cohorts with no returning customers in a given eligible month contribute zero to the consolidated rate.

| KPI | M1 | M3 | M6 |
|---|---:|---:|---:|
| Eligible cohorts | 21 | 19 | 16 |
| Eligible cohort starting buyers | 81,265 | 68,881 | 49,237 |
| Retained buyers | 390 | 180 | 116 |
| **Weighted retention** | **0.48%** | **0.26%** | **0.24%** |

**Observation-window control:** July 2018 is the last fully observed calendar month; August 2018 is excluded from complete-month follow-up. M1, M3, and M6 have **different eligible populations** and do not describe a single fixed cohort. These are non-cumulative month-specific measures.

### RFM variables

| Variable | Average |
|---|---:|
| Analyzed buyers | 93,358 |
| Recency | 238.48 days |
| Frequency | 1.03 orders |
| Historical monetary value | R$141.62 per buyer |

Recency is computed relative to the day after the latest purchase date in the historical dataset, **not today's date**. Monetary value excludes freight.

### Rule-based customer segments

Because 97% of buyers purchased only once, interpretable frequency/recency rules were preferred over frequency quintiles. The **90-day** threshold is exploratory and has not been validated as a churn threshold.

| Segment | Buyers | Share | Historical product value |
|---|---:|---:|---:|
| Older one-time buyers | 72,778 | 77.96% | R$10,035,714.16 |
| Recent first-time buyers | 17,779 | 19.04% | R$2,457,375.20 |
| Older repeat buyers | 2,190 | 2.35% | R$563,538.66 |
| Recent repeat buyers | 611 | 0.65% | R$164,870.09 |
| **Total** | **93,358** | **100%** | **R$13,221,498.11** |

**Note:** “recent” and “older” are relative to the dataset's historical end date and do not indicate current customer status.

## Business insights and recommendations

1. **Second-purchase conversion:** the high one-time buyer share (97.00%) supports investigating the post-purchase journey and testing targeted incentives for recent first-time buyers.
2. **Reactivation:** assess differentiated pilot campaigns for historically repeat buyers with recency above 90 days before adopting a firm inactivity threshold.
3. **Impact measurement:** measure incremental repurchase, incremental contribution margin, and intervention cost. Historical segment revenue is **not** a recoverable-revenue estimate.
4. **Further research:** incorporate product categories and promotional calendars to test whether expected purchase frequency varies by purchase type.

These are **hypotheses, not established causal conclusions**.

## Methodological comparison with Online Retail II

| KPI | Online Retail II | Olist |
|---|---:|---:|
| Analyzed buyers | 5,852 | 93,358 |
| Repeat buyers | 4,234 | 2,801 |
| Observed repeat purchase rate | 72.35% | 3.00% |
| M1 retention | 23.34% | 0.48% |
| M3 retention | 24.98% | 0.26% |
| M6 retention | 22.17% | 0.24% |

This is a **descriptive comparison, not a performance benchmark**. Online Retail II applies its `incluir_recompra = 1` business rule, while Olist uses delivered orders. The businesses, observation periods, operating models, and customer populations differ. Cohort eligibility and measurement conventions also need to be considered when interpreting the rates.

## SQL structure and reproducibility

SQL scripts are located in [`../sql/`](../sql/):

1. `00_estructura_olist.sql` — table structure.
2. `01_vw_pedidos_analiticos.sql` — one delivered order per row with item aggregates.
3. `02_vw_cohortes_retencion.sql` — monthly cohorts.
4. `03_vw_rfm_y_segmentos.sql` — RFM variables and customer segmentation.
5. `04_consultas_indicadores_olist.sql` — KPI queries.
6. `05_comparacion_online_retail_ii.sql` — descriptive repurchase comparison.

For reproduction, download the raw CSVs from Kaggle, create and load the PostgreSQL source tables, and then execute the views in dependency order. Raw source datasets are **not published** in this repository. Inspect the versioned SQL in [`../sql/`](../sql/) before running it.

## Limitations

- Historical dataset; not real-time commercial data.
- Delivered orders only; no inference about subsequent refunds or customer-level profit margins.
- No campaign-exposure, causal, or net-profit evidence.
- Recency thresholds are heuristics.
- Recent cohort observation is limited by the dataset end date.

**Use:** educational portfolio project demonstrating SQL, business intelligence, and customer analytics skills.
