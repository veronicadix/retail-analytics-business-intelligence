# Case 2 — Customer Retention & Revenue Growth

## Executive summary

Historical customer analytics project using **Online Retail II** transactions (December 2009–December 2011). Combines **RFM segmentation**, **acquisition cohorts**, **repeat-purchase intervals**, and an **exploratory delayed-repurchase flag** to support evidence-based retention decisions. No live marketing campaigns or causal impact evaluations were performed.

## Business question

Which customers account for the most historical value, how does purchasing activity evolve after acquisition, and which groups deserve further investigation for loyalty or reactivation initiatives?

## Tech stack

PostgreSQL, SQL (window functions, cohorts, percentiles), Python, Pandas, Matplotlib, Seaborn, Jupyter Notebook, Git/GitHub.

## Scope and key findings

- **5,852 identifiable customers** in the RFM base; approximately **£16.36 million** of historical net purchases for this population.
- **25 monthly acquisition cohorts**, with **147 observable cohort-month records** across months 0–6.
- **Champions:** 1,278 customers, accounting for approximately **69.1%** of identified net purchases.
- **At Risk - High Value:** 333 customers; **Hibernating:** 1,511 customers.
- **Weighted monthly activity after acquisition:** month 1 **23.34%** (23 eligible cohorts), month 3 **24.98%** (21 cohorts), month 6 **22.17%** (18 cohorts).
- **30,742 consecutive purchase intervals** from **4,234 repeat customers**; mean **52.12 days**, median **25.03 days**, 75th percentile **62.08 days**, 90th percentile **135.97 days**.
- **892 customers** meet the final exploratory delayed-repurchase rule, with around **£2.42 million** in historical net purchases.

### Delayed-repurchase segment breakdown

| Segment | Customers | Historical net purchases |
|---|---:|---:|
| At Risk - High Value | 306 | £924,156.50 |
| Loyal Customers | 209 | £815,236.41 |
| Champions | 34 | £332,892.98 |
| At Risk | 303 | £311,117.08 |
| Needs Attention | 40 | £38,061.54 |
| **Total** | **892** | **£2,421,464.51** |

**Analytical priority:** examine **306 At Risk - High Value** and **209 Loyal Customers** with delayed repurchase (515 customers; roughly **£1.74 million** in combined historical net purchases). This amount is **not** forecast recoverable revenue.

## Approach

1. Use eligible invoices with valid customer identifiers.
2. Compute R, F, M quintile scores using `NTILE(5)` and assign seven RFM segments.
3. Group customers by first-purchase month and measure **non-consecutive monthly activity** for up to six months, including only observable periods.
4. Apply `LAG` to consecutive invoices, then summarize purchase intervals and percentiles.
5. Flag delayed repurchase when at least two prior intervals exist and elapsed days since last purchase exceed `GREATEST(30, 2 × individual median interval)`.

See [`METODOLOGIA.md`](METODOLOGIA.md) for business definitions and caveats (in Spanish).

## Outputs

- SQL views: `sql/01_rfm_clientes.sql` through `sql/05_oportunidades_reactivacion.sql`.
- Analysis notebook: `python/analisis_retencion.ipynb`.
- Visuals: `visualizaciones/01_cohort_retention_heatmap.png`, `02_rfm_customer_distribution.png`, `03_rfm_revenue_contribution.png`, `04_rfm_recency_frequency.png`, `05_reactivation_opportunities.png`.
- Executive report (Spanish): `resultados/Caso_02_Informe_Ejecutivo_Retencion_ES.docx`.

The SQL scripts rely on previously created Case 1 objects including `facturas_venta` and `vw_valor_clientes`. The CSV exports in `datos/` are derived analytical extracts, not an independent raw dataset.

## Business recommendations

Pilot retention outreach on prioritized groups with a control group; measure incremental repeat purchases, costs and margin, rather than attributing an outcome to descriptive analysis alone. Reassess rule thresholds and RFM tie handling before production use.

## Limitations and roadmap

Historical data only; no assertions about today's customer status. `NTILE(5)` can split ties across scores. Month 6 includes fewer eligible acquisition cohorts than month 1. Historical purchase amounts are not forecasts or guaranteed recoverable revenue. December 2011 is incomplete and excluded from full-month comparisons. **Olist analysis is complete:** an independent analysis of 93,358 customers was conducted, covering repeat purchases (3.00%), monthly cohort retention (M1: 0.48%; M3: 0.26%; M6: 0.24%), RFM metrics, and customer segmentation. The findings are compared methodologically with Online Retail II without merging the datasets. SQL scripts, results, visualizations, and documentation are available in the [Olist analysis](../olist/documentacion/README_EN.md).

## Case 2 Extension — Olist Brazilian E-Commerce

A second customer retention analysis was developed using
the Olist Brazilian E-Commerce dataset, independently
from Online Retail II.

### Key Business Results

| KPI | Result |
|---|---:|
| Unique customers | 93,358 |
| Delivered orders | 96,478 |
| Repeat purchase rate | 3.00% |
| Month 1 retention | 0.48% |
| Month 3 retention | 0.26% |
| Month 6 retention | 0.24% |
| Historical product revenue | BRL 13,221,498.11 |

### Analysis Delivered

- Customer repeat purchase analysis.
- Monthly cohort retention analysis.
- RFM metrics and customer segmentation.
- Identification of commercial opportunities.
- Methodological comparison with Online Retail II.

### Documentation and Deliverables

- [Olist full documentation](../olist/documentacion/README_EN.md)
- [Spanish documentation](../olist/documentacion/README_ES.md)
- [SQL scripts](../olist/sql/)
- [CSV results](../olist/resultados/)
- [Visualizations](../olist/visualizaciones/)
- [Python code](../olist/python/)

### Methodological Considerations

All findings are based on historical transaction data.

Monthly retention is measured for specific months
using eligible acquisition cohorts, rather than
as cumulative retention.

Olist and Online Retail II are analyzed independently.
Customer records and transactions from the two datasets
have not been merged.