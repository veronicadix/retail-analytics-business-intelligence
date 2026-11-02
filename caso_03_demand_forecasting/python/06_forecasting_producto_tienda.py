"""Caso 03 M5 | Evaluacion producto-tienda de baseline estacional (ultimos 28 dias).
No utiliza datos futuros para pronosticar. Lee solo columnas requeridas para ahorrar RAM.
Requisitos: pandas, numpy. Ejecutar desde la raiz del caso 03.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'datos' / 'raw' / 'sales_train_validation.csv'
OUT = ROOT / 'resultados'
OUT.mkdir(parents=True, exist_ok=True)

# 56 dias de entrenamiento inmediatamente anteriores al test de 28 dias.
# M5 validation: d_1 ... d_1913 (el test final comienza en d_1886).
TRAIN = [f'd_{i}' for i in range(1830, 1886)]
TEST = [f'd_{i}' for i in range(1886, 1914)]
COLS = ['id', 'item_id', 'cat_id', 'store_id'] + TRAIN + TEST

if not SOURCE.exists():
    raise FileNotFoundError(f'No se encontro {SOURCE}')

parts = []
for chunk in pd.read_csv(SOURCE, usecols=COLS, chunksize=2500):
    hist = chunk[TRAIN].to_numpy(dtype=np.float64)
    actual = chunk[TEST].to_numpy(dtype=np.float64)
    # Dias de igual posicion semanal: ocho observaciones, cuatro futuras.
    means = hist.reshape(len(chunk), 8, 7).mean(axis=1)
    predicted = np.tile(means, (1, 4))
    err = predicted - actual
    denom = actual.sum(axis=1)
    base = chunk[['id', 'item_id', 'cat_id', 'store_id']].copy()
    base['venta_real_28d'] = denom
    base['pronostico_28d'] = predicted.sum(axis=1)
    base['error_abs_total'] = np.abs(err).sum(axis=1)
    base['error_total'] = err.sum(axis=1)
    base['MAE'] = np.abs(err).mean(axis=1)
    base['WAPE_pct'] = np.where(denom > 0, 100 * base['error_abs_total'] / np.maximum(denom, 1), np.nan)
    base['dias_venta_cero_test'] = (actual == 0).sum(axis=1)
    base['dias_venta_cero_train'] = (hist == 0).sum(axis=1)
    parts.append(base)

res = pd.concat(parts, ignore_index=True)
res.to_csv(OUT / 'metricas_producto_tienda_28d.csv', index=False, float_format='%.4f')

agg = (res.groupby(['store_id', 'cat_id'], as_index=False)
       [['venta_real_28d', 'pronostico_28d', 'error_abs_total', 'error_total']].sum())
agg['WAPE_micro_producto_pct'] = np.where(agg.venta_real_28d > 0, 100 * agg.error_abs_total / agg.venta_real_28d, np.nan)
agg['Sesgo_pct'] = np.where(agg.venta_real_28d > 0, 100 * agg.error_total / agg.venta_real_28d, np.nan)
agg.to_csv(OUT / 'diagnostico_producto_tienda_por_segmento.csv', index=False, float_format='%.4f')

total_actual = float(res.venta_real_28d.sum())
summary = {
    'periodo_test': '2016-03-28 a 2016-04-24',
    'modelo': 'Media 8 semanas del mismo dia de semana, por producto-tienda',
    'series': int(len(res)),
    'series_sin_ventas_en_test': int((res.venta_real_28d == 0).sum()),
    'series_con_28_dias_cero_en_entrenamiento': int((res.dias_venta_cero_train == 56).sum()),
    'WAPE_micro_producto_pct': round(100 * float(res.error_abs_total.sum()) / total_actual, 4) if total_actual else None,
    'Sesgo_global_pct': round(100 * float(res.error_total.sum()) / total_actual, 4) if total_actual else None,
    'MAE_por_producto_dia': round(float(res.MAE.mean()), 4),
    'nota': 'WAPE micro a nivel producto no es equivalente a WAPE de demanda agregada. No usar WAPE individual cuando venta real = 0.'
}
(OUT / 'resumen_producto_tienda_28d.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print('EVALUACION PRODUCTO-TIENDA |', summary['periodo_test'])
for k, v in summary.items():
    if k not in ('periodo_test', 'nota'): print(f'{k}: {v}')
print('\nCinco segmentos con mayor WAPE micro producto:')
print(agg.sort_values('WAPE_micro_producto_pct', ascending=False)[['store_id', 'cat_id', 'WAPE_micro_producto_pct']].head(5).to_string(index=False))
print('\nArchivos creados en resultados/:')
for f in ['metricas_producto_tienda_28d.csv', 'diagnostico_producto_tienda_por_segmento.csv', 'resumen_producto_tienda_28d.json']:
    print(' -', f)
