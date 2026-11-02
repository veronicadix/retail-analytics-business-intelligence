"""Caso 03: análisis económico de escenarios simulados de inventario M5.

Entradas: resultados/comparacion_simulacion_inventario_28d.csv del script 09.
Los costes son supuestos editables, NO datos de Walmart.
Ejecutar desde la raíz de caso_03_demand_forecasting:
    python python/10_analisis_costos_inventario.py
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'resultados' / 'comparacion_simulacion_inventario_28d.csv'
OUT = ROOT / 'resultados'
OUT.mkdir(exist_ok=True)

# Valores ilustrativos en USD, modificables para escenarios empresariales.
# Coste de mantener 1 unidad de inventario promedio durante los 28 dias.
HOLDING_COSTS_28D = [0.10, 0.50, 1.00, 2.00]
# Penalización económica estimada por 1 unidad de demanda no atendida.
SHORTAGE_COSTS = [1.00, 3.00, 5.00, 10.00]

required = {'escenario', 'demanda_real_test', 'demanda_atendida',
            'demanda_no_atendida', 'inventario_medio_unidades', 'unidades_ordenadas'}
if not INPUT.exists():
    raise SystemExit(f'No existe {INPUT}. Primero ejecuta el script 09.')
df = pd.read_csv(INPUT)
missing = required - set(df.columns)
if missing:
    raise SystemExit(f'Faltan columnas en el archivo 09: {sorted(missing)}')
for c in required - {'escenario'}:
    df[c] = pd.to_numeric(df[c], errors='raise')
if df['escenario'].duplicated().any():
    raise SystemExit('Hay escenarios duplicados; revisar archivo 09.')
if not {'sin_buffer', 'buffer_7_dias'}.issubset(set(df['escenario'])):
    raise SystemExit('No se encontraron los escenarios sin_buffer y buffer_7_dias.')
df = df.set_index('escenario').loc[['sin_buffer', 'buffer_7_dias']].reset_index()

base = df.set_index('escenario')
extra_stock = float(base.loc['buffer_7_dias','inventario_medio_unidades'] - base.loc['sin_buffer','inventario_medio_unidades'])
extra_served = float(base.loc['buffer_7_dias','demanda_atendida'] - base.loc['sin_buffer','demanda_atendida'])
if extra_served <= 0:
    raise SystemExit('El escenario con buffer no atendió más demanda; revisar interpretación.')

rows = []
for h in HOLDING_COSTS_28D:
    for p in SHORTAGE_COSTS:
        costs = {}
        for _, r in df.iterrows():
            cost_h = float(r['inventario_medio_unidades']) * h
            cost_s = float(r['demanda_no_atendida']) * p
            costs[r['escenario']] = cost_h + cost_s
            rows.append({
                'costo_mantener_unidad_28d_usd': h,
                'costo_faltante_unidad_usd': p,
                'escenario': r['escenario'],
                'costo_inventario_usd': round(cost_h, 2),
                'costo_faltantes_usd': round(cost_s, 2),
                'costo_total_supuesto_usd': round(cost_h + cost_s, 2)
            })

out = pd.DataFrame(rows)
out.to_csv(OUT / 'sensibilidad_costos_inventario.csv', index=False, encoding='utf-8-sig')
summary = []
for h in HOLDING_COSTS_28D:
    breakeven = h * extra_stock / extra_served
    summary.append({'costo_mantener_unidad_28d_usd': h,
                    'costo_faltante_equilibrio_usd': round(breakeven, 4),
                    'inventario_medio_adicional_unidades': extra_stock,
                    'unidades_adicionales_atendidas': extra_served})
break_df = pd.DataFrame(summary)
break_df.to_csv(OUT / 'umbral_costo_faltante.csv', index=False, encoding='utf-8-sig')

comparison = out.pivot_table(index=['costo_mantener_unidad_28d_usd','costo_faltante_unidad_usd'],
                             columns='escenario', values='costo_total_supuesto_usd').reset_index()
comparison['ahorro_buffer_vs_sin_usd'] = (comparison['sin_buffer'] - comparison['buffer_7_dias']).round(2)
comparison['escenario_menor_costo'] = comparison['ahorro_buffer_vs_sin_usd'].apply(
    lambda x: 'buffer_7_dias' if x > 0 else ('sin_buffer' if x < 0 else 'empate'))
comparison.to_csv(OUT / 'comparacion_economica_escenarios.csv', index=False, encoding='utf-8-sig')

metadata = {
    'periodo': '28 dias de test; supuestos economicos ilustrativos',
    'nota': 'Evaluacion de sensibilidad, no optimizacion ni utilidad financiera real.',
    'formula': 'costo_total = inventario_medio * costo_mantener_unidad_28d + demanda_no_atendida * costo_faltante_unidad',
    'excluidos': ['costo de compra','margen real','costos de pedido','restricciones de capital','descuentos','caducidad'],
    'inventario_medio_adicional': extra_stock,
    'demanda_adicional_atendida': extra_served,
}
(OUT / 'metodologia_costos_inventario.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
print('ANALISIS DE SENSIBILIDAD DE COSTOS (supuestos en USD):')
print(comparison.to_string(index=False, formatters={'ahorro_buffer_vs_sin_usd':'{:,.2f}'.format}))
print('\nCOSTO DE FALTANTE DE EQUILIBRIO, POR COSTO DE INVENTARIO:')
print(break_df[['costo_mantener_unidad_28d_usd','costo_faltante_equilibrio_usd']].to_string(index=False))
print('\nArchivos creados en resultados/: sensibilidad_costos_inventario.csv, comparacion_economica_escenarios.csv, umbral_costo_faltante.csv, metodologia_costos_inventario.json')
