"""Caso 03 — Simulación ilustrativa de reposición periódica por producto-tienda.

Ejecutar desde la raíz del caso: python python/09_simulacion_reposicion_m5.py
Entradas: datos/raw/sales_train_validation.csv.
Horizonte evaluación: d_1886..d_1913; pronósticos calculados con d_1830..d_1885.
IMPORTANTE: M5 NO proporciona inventario ni lead times reales: todos los
inventarios, recepciones, restricciones y niveles de servicio son simulados.
El test se usa SOLO para simular la demanda realizada, no para pronosticar.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'datos' / 'raw' / 'sales_train_validation.csv'
OUT = ROOT / 'resultados'
OUT.mkdir(exist_ok=True, parents=True)

TRAIN_COLS = [f'd_{i}' for i in range(1830, 1886)]
TEST_COLS = [f'd_{i}' for i in range(1886, 1914)]
LEAD_DAYS = 7  # supuesto
REVIEW_DAYS = 7  # supuesto
COVERAGE_DAYS = LEAD_DAYS + REVIEW_DAYS
SCENARIOS = {'sin_buffer': 0, 'buffer_7_dias': 7}


def simulate(demand, pred_day, buffer_days):
    """Simulación con ventas perdidas, cero backorders y sin restricción de proveedor."""
    n = len(demand)
    avg = pred_day.mean(axis=1)
    # Inicialización hipotética equivalente a 14 días de demanda prevista.
    stock = np.ceil(avg * COVERAGE_DAYS).astype(np.float64)
    pipeline = np.zeros((n, demand.shape[1] + LEAD_DAYS + 1), dtype=np.float64)
    sold = np.zeros(n, dtype=np.float64)
    lost = np.zeros(n, dtype=np.float64)
    ordered = np.zeros(n, dtype=np.float64)
    end_stock_daily = np.zeros(n, dtype=np.float64)
    for day in range(demand.shape[1]):
        stock += pipeline[:, day]
        if day % REVIEW_DAYS == 0:
            # Objetivo simple expresado en días promedio, no optimización de costes.
            target = np.ceil(avg * (COVERAGE_DAYS + buffer_days))
            position = stock + pipeline[:, day + 1:].sum(axis=1)
            qty = np.maximum(0, target - position)
            pipeline[:, day + LEAD_DAYS] += qty
            ordered += qty
        sold_today = np.minimum(stock, demand[:, day])
        sold += sold_today
        lost += demand[:, day] - sold_today
        stock -= sold_today
        end_stock_daily += stock
    return {'demanda': float(demand.sum()), 'ventas_atendidas': float(sold.sum()),
            'ventas_no_atendidas': float(lost.sum()), 'unidades_ordenadas': float(ordered.sum()),
            'inventario_final': float(stock.sum()),
            'inventario_promedio_total_unidades': float(end_stock_daily.sum() / demand.shape[1])}


def main():
    if not SOURCE.exists():
        raise SystemExit(f'Archivo no encontrado: {SOURCE}')
    print('[1/3] Simulando 2 escenarios de inventario con supuestos explícitos...')
    aggregates = {key: {k: 0.0 for k in ('demanda', 'ventas_atendidas', 'ventas_no_atendidas',
                    'unidades_ordenadas', 'inventario_final', 'inventario_promedio_total_unidades')}
                  for key in SCENARIOS}
    segment_metrics = {}
    count = 0
    for chunk in pd.read_csv(SOURCE, usecols=['id', 'store_id', 'cat_id'] + TRAIN_COLS + TEST_COLS, chunksize=1500):
        train = chunk[TRAIN_COLS].to_numpy(dtype=np.float64)
        demand = chunk[TEST_COLS].to_numpy(dtype=np.float64)
        # Predicción semanal media de 8 semanas; no toca el test.
        pred_week = train.reshape(-1, 8, 7).mean(axis=1)
        predicted = np.tile(pred_week, (1, 4))
        count += len(chunk)
        for scenario, buffer in SCENARIOS.items():
            res = simulate(demand, predicted, buffer)
            for metric, value in res.items():
                aggregates[scenario][metric] += value
            for (store, cat), sub in chunk.groupby(['store_id', 'cat_id'], sort=False):
                mask = (chunk['store_id'].to_numpy() == store) & (chunk['cat_id'].to_numpy() == cat)
                sm = simulate(demand[mask], predicted[mask], buffer)
                key = (scenario, store, cat)
                target = segment_metrics.setdefault(key, {k: 0.0 for k in res})
                for metric, value in sm.items():
                    target[metric] += value
    print('[2/3] Consolidando métricas...')
    rows = []
    for scenario, m in aggregates.items():
        rows.append({'escenario': scenario, 'series': count, 'demanda_real_test': round(m['demanda']),
                     'demanda_atendida': round(m['ventas_atendidas']),
                     'demanda_no_atendida': round(m['ventas_no_atendidas']),
                     'fill_rate_pct': round(100 * m['ventas_atendidas']/m['demanda'], 2) if m['demanda'] else None,
                     'unidades_ordenadas': round(m['unidades_ordenadas']),
                     'inventario_final': round(m['inventario_final']),
                     'inventario_medio_unidades': round(m['inventario_promedio_total_unidades'])})
    pd.DataFrame(rows).to_csv(OUT/'comparacion_simulacion_inventario_28d.csv', index=False, encoding='utf-8-sig')
    segrows = []
    for (scenario, store, cat), m in segment_metrics.items():
        segrows.append({'escenario':scenario,'store_id':store,'cat_id':cat,
                        'demanda_test':round(m['demanda']),
                        'demanda_no_atendida':round(m['ventas_no_atendidas']),
                        'fill_rate_pct':round(100*m['ventas_atendidas']/m['demanda'],2) if m['demanda'] else None,
                        'unidades_ordenadas':round(m['unidades_ordenadas'])})
    pd.DataFrame(segrows).sort_values(['escenario','store_id','cat_id']).to_csv(
        OUT/'simulacion_inventario_por_segmento.csv', index=False, encoding='utf-8-sig')
    report = {'modelo_pronostico':'Dia_semana_8s (producto-tienda)',
              'test':'d_1886..d_1913', 'supuestos': {'lead_time_dias':LEAD_DAYS,
              'revision_cada_dias':REVIEW_DAYS,'inventario_inicial':'14 dias de pronostico medio por producto-tienda',
              'buffer_dias_por_escenario':SCENARIOS,'ventas_no_atendidas':'perdidas, no backorders',
              'proveedor':'capacidad ilimitada', 'restricciones_presupuesto':'ninguna',
              'costes':'no incluidos'}, 'resultados':rows,
              'advertencia':'Simulacion hipotetica: no representa inventario real ni una politica optima.'}
    (OUT/'resumen_simulacion_inventario.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('[3/3] RESULTADOS DE INVENTARIO SIMULADO:')
    print(pd.DataFrame(rows).to_string(index=False))
    print('\nArchivos: comparacion_simulacion_inventario_28d.csv, simulacion_inventario_por_segmento.csv, resumen_simulacion_inventario.json')
    print('IMPORTANTE: stock, lead time y pedidos son supuestos, no datos observados.')


if __name__ == '__main__':
    main()
