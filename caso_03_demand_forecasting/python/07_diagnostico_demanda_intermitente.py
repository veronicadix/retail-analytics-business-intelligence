"""Caso 03 M5 | Diagnostico de patrones de demanda por producto-tienda.

Solo usa ventas d_1718..d_1885 (168 dias) para clasificar la demanda.
Evalua el baseline estacional de 8 semanas en d_1886..d_1913 (28 dias).
La clasificacion es descriptiva y NO selecciona politicas usando el test.
Requisitos: pandas, numpy. Ejecutar desde cualquier carpeta.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'datos' / 'raw' / 'sales_train_validation.csv'
OUT = ROOT / 'resultados'
OUT.mkdir(parents=True, exist_ok=True)
if not SRC.exists():
    raise FileNotFoundError(f'Archivo no encontrado: {SRC}')

H = [f'd_{n}' for n in range(1718, 1886)]
T = [f'd_{n}' for n in range(1886, 1914)]
cols = ['id', 'item_id', 'store_id', 'cat_id'] + H + T
rows = []
for chunk in pd.read_csv(SRC, usecols=cols, chunksize=2000):
    hist = chunk[H].to_numpy(dtype=np.float64)
    test = chunk[T].to_numpy(dtype=np.float64)
    positive = hist > 0
    count = positive.sum(axis=1)
    adi = np.divide(168.0, count, out=np.full(len(chunk), np.nan), where=count > 0)
    mean_nonzero = np.divide(hist.sum(axis=1), count, out=np.zeros(len(chunk)), where=count > 0)
    # Coeficiente de variacion al cuadrado SOLO de demandas positivas.
    deviations = np.where(positive, hist - mean_nonzero[:, None], 0)
    var_nonzero = np.divide((deviations**2).sum(axis=1), count, out=np.zeros(len(chunk)), where=count > 0)
    cv2 = np.divide(var_nonzero, mean_nonzero**2, out=np.full(len(chunk), np.nan), where=mean_nonzero > 0)
    group = np.full(len(chunk), 'Sin demanda historica', dtype=object)
    eligible = count > 0
    group[eligible & (adi < 1.32) & (cv2 < 0.49)] = 'Regular'
    group[eligible & (adi < 1.32) & (cv2 >= 0.49)] = 'Erratica'
    group[eligible & (adi >= 1.32) & (cv2 < 0.49)] = 'Intermitente'
    group[eligible & (adi >= 1.32) & (cv2 >= 0.49)] = 'Irregular intermitente'
    recent = hist[:, -56:]
    prediction = np.tile(recent.reshape(len(chunk), 8, 7).mean(axis=1), (1, 4))
    diff = prediction - test
    part = chunk[['id', 'item_id', 'store_id', 'cat_id']].copy()
    part['tipo_demanda'] = group
    part['dias_con_ventas_hist_168d'] = count
    part['ADI'] = adi
    part['CV2'] = cv2
    part['unidades_reales_28d'] = test.sum(axis=1)
    part['unidades_previstas_28d'] = prediction.sum(axis=1)
    part['error_absoluto_28d'] = np.abs(diff).sum(axis=1)
    part['error_firmado_28d'] = diff.sum(axis=1)
    part['dias_con_ventas_test'] = (test > 0).sum(axis=1)
    rows.append(part)

res = pd.concat(rows, ignore_index=True)
res.to_csv(OUT / 'clasificacion_demanda_producto_tienda.csv', index=False, float_format='%.4f')
summary = res.groupby('tipo_demanda', as_index=False).agg(
    series=('id', 'size'), unidades_reales_28d=('unidades_reales_28d', 'sum'),
    unidades_previstas_28d=('unidades_previstas_28d', 'sum'),
    error_absoluto_28d=('error_absoluto_28d', 'sum'),
    error_firmado_28d=('error_firmado_28d', 'sum'),
    sin_ventas_test=('unidades_reales_28d', lambda x: int((x == 0).sum()))
)
summary['participacion_series_pct'] = 100 * summary.series / summary.series.sum()
summary['WAPE_micro_pct'] = np.where(summary.unidades_reales_28d > 0,
    100 * summary.error_absoluto_28d / summary.unidades_reales_28d, np.nan)
summary['sesgo_pct'] = np.where(summary.unidades_reales_28d > 0,
    100 * summary.error_firmado_28d / summary.unidades_reales_28d, np.nan)
summary.to_csv(OUT / 'resumen_patrones_demanda.csv', index=False, float_format='%.4f')
print('DIAGNOSTICO DE DEMANDA | entrenamiento d_1718..d_1885 | test d_1886..d_1913')
print('Criterios descriptivos: ADI 1.32 y CV2 0.49; sin demanda positiva = categoria separada.')
print(summary[['tipo_demanda', 'series', 'participacion_series_pct', 'WAPE_micro_pct', 'sin_ventas_test']].round(2).to_string(index=False))
print('\nWAPE general micro producto: %.3f %%' % (100 * res.error_absoluto_28d.sum() / res.unidades_reales_28d.sum()))
print('Archivos: resultados/clasificacion_demanda_producto_tienda.csv y resultados/resumen_patrones_demanda.csv')
