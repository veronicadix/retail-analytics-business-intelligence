"""Caso 03: evaluación de baselines de pronóstico diario agregado M5.

Ejecutar desde cualquier ubicación:
    python python/02_baseline_forecasting_m5.py
Requiere: pandas, numpy, matplotlib.

No lee datos futuros para formular los pronósticos del holdout ni edita CSV originales.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'resultados' / 'ventas_diarias_m5.csv'
OUT = ROOT / 'resultados'
FIG = ROOT / 'visualizaciones'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
HORIZON = 28


def forecasts(train, future_dates):
    y = train['unidades'].to_numpy(dtype=float)
    if len(y) < 56:
        raise ValueError('Se requieren al menos 56 dias de entrenamiento.')
    # Semana reciente repetida 4 veces. Pronostico fijo, sin actualizarse con holdout.
    naive_7 = np.tile(y[-7:], int(np.ceil(len(future_dates) / 7)))[:len(future_dates)]
    mean28 = np.full(len(future_dates), y[-28:].mean())
    # Promedio de cada dia de semana en las ultimas 8 semanas del entrenamiento.
    last56 = train.tail(56).copy()
    weekly = last56.groupby(last56['date'].dt.dayofweek)['unidades'].mean()
    dow8 = np.array([weekly[d.dayofweek] for d in future_dates], dtype=float)
    return {'Naive_7': naive_7, 'Media_28': mean28, 'Dia_semana_8s': dow8}


def metrics(actual, predicted):
    err = predicted - actual
    return {
        'MAE': float(np.abs(err).mean()),
        'WAPE_pct': float(np.abs(err).sum() / actual.sum() * 100) if actual.sum() else None,
        'Sesgo_pct': float(err.sum() / actual.sum() * 100) if actual.sum() else None,
    }


def main():
    if not SRC.exists():
        raise FileNotFoundError(f'Falta {SRC}. Ejecuta primero 01_exploracion_m5.py')
    df = pd.read_csv(SRC, parse_dates=['date'])
    if not {'date', 'unidades'}.issubset(df.columns):
        raise ValueError('ventas_diarias_m5.csv requiere columnas date y unidades.')
    df = df[['date', 'unidades']].sort_values('date').reset_index(drop=True)
    if df['date'].isna().any() or df['unidades'].isna().any() or df['date'].duplicated().any():
        raise ValueError('Fechas duplicadas o valores nulos en serie diaria.')
    if not (df['date'].diff().iloc[1:] == pd.Timedelta(days=1)).all():
        raise ValueError('La serie diaria tiene saltos de fecha.')
    train, test = df.iloc[:-HORIZON], df.iloc[-HORIZON:]
    candidate = forecasts(train, test['date'])
    real = test['unidades'].to_numpy(dtype=float)
    report = []
    comparison = test.rename(columns={'unidades':'real'}).copy()
    for name, pred in candidate.items():
        comparison[name] = np.rint(np.maximum(pred, 0)).astype(int)
        report.append({'modelo':name, **metrics(real, pred)})
    report_df = pd.DataFrame(report).sort_values('WAPE_pct')
    winner = report_df.iloc[0]['modelo']
    comparison.to_csv(OUT / 'comparacion_baselines_28d.csv', index=False, encoding='utf-8-sig')
    report_df.to_csv(OUT / 'metricas_baselines_28d.csv', index=False, encoding='utf-8-sig')
    summary = {
        'nivel': 'ventas diarias agregadas de todas las tiendas y productos',
        'fecha_inicio_entrenamiento': str(train['date'].min().date()),
        'fecha_fin_entrenamiento': str(train['date'].max().date()),
        'fecha_inicio_prueba': str(test['date'].min().date()),
        'fecha_fin_prueba': str(test['date'].max().date()),
        'horizonte_dias': HORIZON,
        'mejor_baseline_por_WAPE': winner,
        'metricas': report_df.to_dict(orient='records'),
        'nota': 'Evaluacion holdout unica: no demuestra generalizacion. No se usa stock real ni es aun un modelo por SKU.'
    }
    (OUT / 'resumen_baselines_28d.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(test['date'], real, color='black', linewidth=2, label='Ventas reales')
    for name, pred in candidate.items():
        ax.plot(test['date'], pred, linewidth=1.5, label=name)
    ax.set(title='M5 · Pronosticos de 28 dias (holdout)', xlabel='Fecha', ylabel='Unidades diarias')
    ax.legend()
    ax.grid(alpha=.2)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(FIG / '03_comparacion_baselines_28d.png', dpi=160)
    plt.close(fig)
    print('\nPERIODO DE PRUEBA:', str(test['date'].min().date()), 'a', str(test['date'].max().date()))
    print(report_df.to_string(index=False, float_format=lambda x: f'{x:,.2f}'))
    print('\nMejor baseline por WAPE:', winner)
    print('Archivos creados:')
    for p in ['resultados/comparacion_baselines_28d.csv', 'resultados/metricas_baselines_28d.csv', 'resultados/resumen_baselines_28d.json', 'visualizaciones/03_comparacion_baselines_28d.png']:
        print(' -', p)

if __name__ == '__main__':
    main()
