"""Caso 03 · Exploración inicial de M5 Forecasting.

Ejecutar desde la raíz de caso_03_demand_forecasting:
    python python/01_exploracion_m5.py

Dependencias: pandas, numpy, matplotlib.
"""
from pathlib import Path
import csv
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "datos" / "raw"
RESULTS = ROOT / "resultados"
FIGURES = ROOT / "visualizaciones"
RESULTS.mkdir(exist_ok=True, parents=True)
FIGURES.mkdir(exist_ok=True, parents=True)


def main():
    names = ["calendar.csv", "sell_prices.csv", "sales_train_validation.csv"]
    missing = [n for n in names if not (RAW / n).is_file()]
    if missing:
        raise FileNotFoundError(f"No se encontraron en {RAW}: {', '.join(missing)}")

    print("[1/4] Leyendo calendario y precios...")
    calendar = pd.read_csv(RAW / "calendar.csv", usecols=["date", "d", "wm_yr_wk", "event_name_1", "snap_CA", "snap_TX", "snap_WI"], parse_dates=["date"])
    price_cols = ["store_id", "item_id", "wm_yr_wk", "sell_price"]
    prices = pd.read_csv(RAW / "sell_prices.csv", usecols=price_cols, dtype={"store_id": "category", "item_id": "category", "wm_yr_wk": "int32", "sell_price": "float32"})

    print("[2/4] Procesando ventas en bloques para controlar memoria...")
    # Las ~30.490 series x 1.913 días se leen por bloques de filas.
    with open(RAW / "sales_train_validation.csv", encoding="utf-8-sig", newline="") as fp:
        header = next(csv.reader(fp))
    days = [c for c in header if c.startswith("d_")]
    dimensions = ["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"]
    totals = pd.Series(0, index=days, dtype="int64")
    by_cat = {}
    by_store = {}
    n_series = 0
    missing_units = 0

    for chunk in pd.read_csv(RAW / "sales_train_validation.csv", chunksize=500, dtype={d: "int16" for d in days}):
        n_series += len(chunk)
        missing_units += int(chunk[days].isna().sum().sum())
        totals = totals.add(chunk[days].sum(axis=0).astype("int64"), fill_value=0).astype("int64")
        for category, group in chunk.groupby("cat_id"):
            by_cat[category] = by_cat.get(category, 0) + int(group[days].to_numpy().sum())
        for store, group in chunk.groupby("store_id"):
            by_store[store] = by_store.get(store, 0) + int(group[days].to_numpy().sum())
        print(f"    Series procesadas: {n_series:,}")

    daily = pd.DataFrame({"d": days, "unidades": totals.values})
    daily = daily.merge(calendar[["d", "date"]], how="left", on="d", validate="one_to_one").sort_values("date")
    daily.to_csv(RESULTS / "ventas_diarias_m5.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame(sorted(by_cat.items()), columns=["categoria", "unidades"]).to_csv(RESULTS / "ventas_por_categoria.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(sorted(by_store.items()), columns=["tienda", "unidades"]).to_csv(RESULTS / "ventas_por_tienda.csv", index=False, encoding="utf-8-sig")

    print("[3/4] Creando gráfico de tendencia y estacionalidad...")
    daily["media_28d"] = daily["unidades"].rolling(28, min_periods=28).mean()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(daily["date"], daily["unidades"], label="Unidades diarias", linewidth=.6, alpha=.45)
    ax.plot(daily["date"], daily["media_28d"], label="Promedio móvil 28 días", linewidth=1.5)
    ax.set(xlabel="Fecha", ylabel="Unidades", title="M5 · Ventas diarias agregadas")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "01_ventas_diarias_m5.png", dpi=160)
    plt.close(fig)

    daily["dia_semana"] = daily["date"].dt.dayofweek
    weekly = daily.groupby("dia_semana")["unidades"].mean().reindex(range(7))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"], weekly)
    ax.set(xlabel="Día de semana", ylabel="Unidades promedio", title="M5 · Estacionalidad semanal")
    fig.tight_layout()
    fig.savefig(FIGURES / "02_estacionalidad_semanal.png", dpi=160)
    plt.close(fig)

    print("[4/4] Guardando resumen...")
    summary = {
        "dataset": "M5 Forecasting Accuracy (sales_train_validation)",
        "series_producto_tienda": n_series,
        "dias_historicos": len(days),
        "fecha_inicio": str(daily["date"].min().date()),
        "fecha_fin": str(daily["date"].max().date()),
        "unidades_totales": int(daily["unidades"].sum()),
        "valores_nulos_ventas": missing_units,
        "fechas_sin_coincidencia_calendario": int(daily["date"].isna().sum()),
        "filas_calendario": len(calendar),
        "filas_precios": len(prices),
        "precios_nulos": int(prices["sell_price"].isna().sum()),
        "categorias": by_cat,
        "tiendas": by_store,
        "nota": "Exploración descriptiva. No son métricas de desempeño predictivo."
    }
    (RESULTS / "resumen_exploracion_m5.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nOK. Resultados:")
    for f in sorted(RESULTS.glob("*m5*")):
        print(" -", f.relative_to(ROOT))
    print(" -", (RESULTS / "ventas_por_categoria.csv").relative_to(ROOT))
    print(" -", (RESULTS / "ventas_por_tienda.csv").relative_to(ROOT))
    print(" -", (FIGURES / "01_ventas_diarias_m5.png").relative_to(ROOT))
    print(" -", (FIGURES / "02_estacionalidad_semanal.png").relative_to(ROOT))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
