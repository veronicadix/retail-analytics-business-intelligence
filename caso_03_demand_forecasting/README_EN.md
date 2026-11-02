# Case 03 | Demand Forecasting & Inventory Planning

**Retail Analytics & Business Intelligence | Portfolio Project**

## Business question
How can a retailer forecast sales by store and product, and assess the trade-off between product availability and additional inventory? This project combines historical retail time series, forecasting evaluation, intermittent-demand diagnostics, and **hypothetical** replenishment and cost scenarios.

## Data and evaluation
- **Dataset:** M5 Forecasting Accuracy (historical Walmart sales published for the M5 competition).
- **Historical span:** January 29, 2011–April 24, 2016; 1,913 daily observations in the validation training file.
- **Granularity:** 30,490 product-store series across 10 stores and 3 categories.
- **Held-out test:** March 28–April 24, 2016 (28 days; `d_1886`–`d_1913`).
- **Main inputs:** `sales_train_validation.csv`, `calendar.csv`, `sell_prices.csv`.

> M5 sales are historical observations. Inventory balances, replenishment orders, lead times, buffers, and monetary costs in this project are **assumptions**, not observed Walmart operations.

## Workflow
1. Explore demand trends, calendar patterns, stores, categories, and data quality.
2. Benchmark naive weekly, 28-day mean, and same-weekday eight-week average (`Dia_semana_8s`); test a trend-enhanced alternative.
3. Evaluate 30 store-category segments with time-based validation.
4. Forecast 30,490 individual product-store series.
5. Diagnose demand with ADI and CV² (168-day classification window), and compare Croston-SBA variants.
6. Simulate two replenishment scenarios with and without a seven-day buffer.
7. Run illustrative cost-sensitivity analysis to expose the service-level versus inventory trade-off.

## Forecast results

| Level / approach | WAPE | Finding |
|---|---:|---|
| Aggregate, same-weekday eight-week mean | **5.52%** | Best tested aggregate baseline |
| Aggregate, weekly trend | 6.55% | Did not improve the baseline |
| Store-category, same-weekday eight-week mean | **9.33%** | Best tested segmented global policy |
| Store-category, validation-selected policy | 9.52% | No improvement |
| Product-store, same-weekday eight-week mean | **76.217%** | Highly challenging item-level accuracy |
| Product-store, Croston-SBA α=0.1 | 78.1035% | Did not improve global accuracy |
| Product-store, Croston-SBA α=0.2 | 78.5082% | Did not improve global accuracy |

**Important:** WAPE values across aggregation levels should not be interpreted as directly interchangeable because forecast errors offset differently.

### Demand patterns
Out of 30,490 product-store series, 22,986 (75.39%) were classified as intermittent and 3,176 (10.42%) as lumpy/intermittent-irregular demand. The remaining groups were regular (3,295), erratic (703), or without positive historical demand in the analysis window (330). Descriptive ADI and CV² thresholds: 1.32 and 0.49.

## Replenishment scenario results (28 days)

| Metric | No buffer | 7-day buffer |
|---|---:|---:|
| Historical test sales demand used in simulation | 1,183,626 | 1,183,626 |
| Simulated demand fulfilled | 985,097 | 1,107,316 |
| Simulated unfulfilled demand | 198,529 | 76,310 |
| **Simulated fill rate** | **83.23%** | **93.55%** |
| Simulated units ordered | 759,451 | 1,139,915 |
| Simulated ending stock | 119,777 | 356,190 |
| Simulated mean inventory | 269,815 | 458,951 |

The buffer scenario fulfills **122,219 additional units** (+10.32 percentage points in fill rate), but requires **189,136 additional units** of mean inventory (approximately +70.10%).

### Operational assumptions
- Fixed 7-day lead time and 7-day inventory review cycle.
- Initial inventory set to the equivalent of 14 days of average predicted demand by product-store series.
- Additional safety buffer of either 0 or 7 days of expected demand.
- Unfulfilled demand is treated as lost sales (no backorders).
- Unlimited supplier capacity; no budget constraints.

## Illustrative economic sensitivity

`total_cost = average_inventory × holding_cost_per_unit_for_28_days + unfulfilled_demand × shortage_cost_per_unit`

| Holding cost per unit / 28 days | Break-even shortage cost per unit |
|---:|---:|
| US$0.10 | US$0.1548 |
| US$0.50 | US$0.7738 |
| US$1.00 | US$1.5475 |
| US$2.00 | US$3.0950 |

Under this simplified cost model, the seven-day buffer has the lower calculated cost in 13 of 16 tested combinations. This **does not measure real profit or savings**. Purchase costs, actual margins, ordering costs, capital constraints, discounts, and expiration were excluded; the analysis is not an inventory optimization.

## Project structure

```text
caso_03_demand_forecasting/
├── datos/raw/             # Download the original CSVs separately
├── datos/procesados/
├── documentacion/         # Business and methodology reports
├── python/                # Scripts 01–10
├── resultados/            # Generated metrics and JSON/CSV exports
├── sql/
├── visualizaciones/       # Generated charts
├── README.md              # Spanish overview
└── README_EN.md           # This English overview
```

## Reproduce
1. Download the data from [M5 Forecasting Accuracy on Kaggle](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data), observing its terms.
2. Extract the input CSV files to `datos/raw/`.
3. Install the Python dependencies: `python -m pip install pandas numpy matplotlib`.
4. Run scripts in `python/` in numeric order from **01 to 10**, starting from the Case 03 project directory.
5. Review generated `resultados/` and `visualizaciones/`.

Before publication, pin and test dependency versions, review generated output size, and exclude large source datasets, ZIP files, and credentials from GitHub.

## Caveats and future work
- Product-store WAPE is high: these forecasts should not be presented as production-ready ordering recommendations.
- Historical sales may not reveal unmet demand, so recorded sales are not necessarily unconstrained demand.
- Real inventory positions, variable lead times, purchasing constraints, and complete costs are not available.
- Reported final test results cover **one 28-day period**; operational deployment would require further rolling validation and monitoring.

**Skills:** Python · pandas · NumPy · Matplotlib · Time Series · Forecast Error Measurement · Demand Segmentation · Inventory Planning · Scenario Analysis · Business Intelligence.
