"""Caso 03 — Comparación reproducible: Día_semana_8s frente a Croston-SBA.

Entrada: datos/raw/sales_train_validation.csv (M5).
Prueba final: d_1886 a d_1913 (28 días). No se usan datos de test
para calcular pronósticos ni clasificar demanda.

Requisitos: pandas, numpy.
Uso desde raíz del caso: python python/08_comparacion_croston_sba.py
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "datos" / "raw" / "sales_train_validation.csv"
OUT = ROOT / "resultados"
OUT.mkdir(parents=True, exist_ok=True)

START, TRAIN_END, TEST_END = 1718, 1885, 1913
TRAIN_COLS = [f"d_{i}" for i in range(START, TRAIN_END + 1)]
TEST_COLS = [f"d_{i}" for i in range(TRAIN_END + 1, TEST_END + 1)]
COLUMNS = ["id", "store_id", "cat_id"] + TRAIN_COLS + TEST_COLS
ALPHAS = (0.1, 0.2)


def croston_sba(x: np.ndarray, alpha: float) -> np.ndarray:
    """Vectorizado por series; pronóstico constante, no negativo.

    Inicialización: primer evento positivo, intervalo hasta primer evento.
    El tiempo entre eventos se mide en días. Sin eventos => cero.
    """
    n, periods = x.shape
    z = np.zeros(n, dtype=np.float64)
    p = np.zeros(n, dtype=np.float64)
    last_event = np.zeros(n, dtype=np.int32)
    started = np.zeros(n, dtype=bool)
    for day in range(1, periods + 1):
        demand = x[:, day - 1]
        active = demand > 0
        first = active & ~started
        z[first] = demand[first]
        p[first] = day
        started[first] = True
        later = active & ~first
        z[later] += alpha * (demand[later] - z[later])
        gap = day - last_event[later]
        p[later] += alpha * (gap - p[later])
        last_event[active] = day
    forecast = np.divide(z, p, out=np.zeros(n), where=p > 0)
    return np.maximum(0.0, (1 - alpha / 2) * forecast)


def classify_demand(x: np.ndarray) -> np.ndarray:
    """ADI=observaciones/eventos positivos; CV² sólo en valores positivos.

    Umbrales descriptivos ADI 1.32, CV² 0.49 (igual que paso 07).
    """
    pos = x > 0
    counts = pos.sum(axis=1)
    adi = np.divide(x.shape[1], counts, out=np.full(len(x), np.inf), where=counts > 0)
    sum_pos = x.sum(axis=1)
    mean_pos = np.divide(sum_pos, counts, out=np.zeros(len(x)), where=counts > 0)
    sum_sq = (x * x).sum(axis=1)
    var_pos = np.divide(sum_sq, counts, out=np.zeros(len(x)), where=counts > 0) - mean_pos**2
    cv2 = np.divide(np.maximum(var_pos, 0), mean_pos**2,
                    out=np.zeros(len(x)), where=mean_pos > 0)
    kinds = np.full(len(x), "Regular", dtype=object)
    kinds[(adi <= 1.32) & (cv2 > 0.49)] = "Erratica"
    kinds[(adi > 1.32) & (cv2 <= 0.49)] = "Intermitente"
    kinds[(adi > 1.32) & (cv2 > 0.49)] = "Irregular intermitente"
    kinds[counts == 0] = "Sin demanda historica"
    return kinds


def safe_wape(error: float, actual: float):
    return round(100 * error / actual, 4) if actual > 0 else None


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Falta archivo de entrada: {SOURCE}")
    forecasts = ["Dia_semana_8s", "Croston_SBA_01", "Croston_SBA_02"]
    overall = {model: {"error": 0.0, "forecast": 0.0} for model in forecasts}
    segments = {}
    records = []
    n_total = 0
    print("[1/3] Lectura de ventas M5 por bloques...")
    for chunk in pd.read_csv(SOURCE, usecols=COLUMNS, chunksize=1500):
        x = chunk[TRAIN_COLS].to_numpy(dtype=np.float64)
        y = chunk[TEST_COLS].to_numpy(dtype=np.float64)
        # 56 días alineados: una predicción por día semanal, repetida cuatro veces.
        week = x[:, -56:].reshape(len(x), 8, 7).mean(axis=1)
        pred_week = np.tile(week, (1, 4))
        f1 = croston_sba(x, 0.1)[:, None]
        f2 = croston_sba(x, 0.2)[:, None]
        pred = {"Dia_semana_8s": pred_week,
                "Croston_SBA_01": np.broadcast_to(f1, y.shape),
                "Croston_SBA_02": np.broadcast_to(f2, y.shape)}
        kinds = classify_demand(x)
        actual = y.sum(axis=1)
        for model, yp in pred.items():
            err = np.abs(y - yp).sum(axis=1)
            total_pred = yp.sum(axis=1)
            overall[model]["error"] += float(err.sum())
            overall[model]["forecast"] += float(total_pred.sum())
            for kind in np.unique(kinds):
                mask = kinds == kind
                key = (kind, model)
                agg = segments.setdefault(key, {"series": 0, "actual": 0., "error": 0., "forecast": 0.})
                agg["series"] += int(mask.sum())
                agg["actual"] += float(actual[mask].sum())
                agg["error"] += float(err[mask].sum())
                agg["forecast"] += float(total_pred[mask].sum())
        for j in range(len(chunk)):
            records.append({"id": str(chunk.iloc[j]["id"]),
                            "store_id": chunk.iloc[j]["store_id"],
                            "cat_id": chunk.iloc[j]["cat_id"],
                            "tipo_demanda": kinds[j],
                            "unidades_reales_test": float(actual[j]),
                            "pred_semana_8s_28d": float(pred_week[j].sum()),
                            "pred_croston_sba_01_28d": float(f1[j, 0] * 28),
                            "pred_croston_sba_02_28d": float(f2[j, 0] * 28)})
        n_total += len(chunk)
    total_actual = sum(r["unidades_reales_test"] for r in records)
    print("[2/3] Calculando métricas con el mismo test (d_1886..d_1913)...")
    summary = []
    for model in forecasts:
        a = overall[model]
        summary.append({"modelo": model, "WAPE_micro_pct": safe_wape(a["error"], total_actual),
                        "sesgo_pct": round(100 * (a["forecast"] - total_actual) / total_actual, 4) if total_actual else None,
                        "MAE_producto_dia": round(a["error"] / (n_total * 28), 5)})
    by_kind = [{"tipo_demanda": kind, "modelo": model, "series": a["series"],
                "unidades_reales": round(a["actual"], 2),
                "WAPE_micro_pct": safe_wape(a["error"], a["actual"]),
                "sesgo_pct": round(100 * (a["forecast"] - a["actual"]) / a["actual"], 4) if a["actual"] else None}
               for (kind, model), a in segments.items()]
    df = pd.DataFrame(summary).sort_values("WAPE_micro_pct")
    df.to_csv(OUT / "metricas_croston_vs_semanal_28d.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(by_kind).sort_values(["tipo_demanda", "WAPE_micro_pct"]).to_csv(
        OUT / "metricas_croston_por_tipo_demanda.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(records).to_csv(OUT / "pronosticos_croston_producto_tienda_28d.csv", index=False, encoding="utf-8-sig")
    report = {"periodo_entrenamiento": f"d_{START}..d_{TRAIN_END}",
              "periodo_prueba": f"d_{TRAIN_END+1}..d_{TEST_END}",
              "series": n_total, "unidades_reales_test": total_actual,
              "comparacion": summary,
              "nota": "Benchmarks exploratorios. No se seleccionó política por tipo con el test. Clasificación hecha sólo con entrenamiento."}
    (OUT / "resumen_croston_vs_semanal.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[3/3] MÉTRICAS TEST FINAL:")
    print(df.to_string(index=False))
    print("\nArchivos generados en resultados/:")
    for name in ["metricas_croston_vs_semanal_28d.csv", "metricas_croston_por_tipo_demanda.csv",
                 "pronosticos_croston_producto_tienda_28d.csv", "resumen_croston_vs_semanal.json"]:
        print(" -", name)
    print("\nNota: Esto compara modelos, no selecciona todavía políticas de reposición.")

if __name__ == "__main__":
    main()
