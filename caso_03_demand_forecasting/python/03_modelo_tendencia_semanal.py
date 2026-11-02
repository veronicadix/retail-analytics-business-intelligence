"""Caso 03 - modelo de tendencia semanal con validación temporal (sin fuga).

Entrada: resultados/ventas_diarias_m5.csv, generado por 01_exploracion_m5.py.
Ejecutar: python python/03_modelo_tendencia_semanal.py
Dependencias: pandas, numpy, matplotlib.

Se eligen hiperparámetros mediante 4 ventanas anteriores de 28 días;
la prueba final de 28 días se mantiene completamente separada.
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
OUT.mkdir(exist_ok=True, parents=True)
FIG.mkdir(exist_ok=True, parents=True)
H = 28
WINDOWS = [84, 168, 364]
REGULARIZATION = [0.0, 14.0, 56.0]


def baseline(training, dates):
    recent = training.tail(56)
    byday = recent.groupby(recent['date'].dt.dayofweek)['unidades'].mean()
    return np.array([byday[d.dayofweek] for d in dates], dtype=float)


def design(dates, origin):
    # Días desde el inicio de la ventana, normalizados a semanas.
    t = ((pd.DatetimeIndex(dates) - origin).days / 7).to_numpy(dtype=float)
    dow = pd.DatetimeIndex(dates).dayofweek.to_numpy()
    # Intercepto + tendencia lineal + seis indicadores de día (lunes base).
    return np.column_stack([np.ones(len(t)), t, *[(dow == d).astype(float) for d in range(1, 7)]])


def forecast(training, dates, window, penalty):
    subset = training.tail(window)
    origin = subset['date'].iloc[0]
    X = design(subset['date'], origin)
    y = subset['unidades'].to_numpy(dtype=float)
    reg = np.diag([0., penalty, *([0.] * 6)])
    # La penalización estabiliza la tendencia, expresada en unidades/semana.
    beta = np.linalg.solve(X.T @ X + reg, X.T @ y)
    return np.maximum(0, design(dates, origin) @ beta)


def metrics(actual, pred):
    difference = pred - actual
    denominator = actual.sum()
    return {'MAE': float(np.abs(difference).mean()),
            'WAPE_pct': float(100 * np.abs(difference).sum() / denominator) if denominator else None,
            'Sesgo_pct': float(100 * difference.sum() / denominator) if denominator else None}


def main():
    if not SRC.exists():
        raise FileNotFoundError(f'No existe {SRC}. Ejecuta antes 01_exploracion_m5.py')
    df = pd.read_csv(SRC, parse_dates=['date'])[['date', 'unidades']].sort_values('date').reset_index(drop=True)
    if df['date'].isna().any() or df['unidades'].isna().any() or df['date'].duplicated().any():
        raise ValueError('Fechas o unidades faltantes, o fechas duplicadas.')
    if not (df['date'].diff().iloc[1:] == pd.Timedelta(days=1)).all():
        raise ValueError('Fechas no consecutivas.')
    if len(df) < 600:
        raise ValueError('Se necesita al menos 600 días.')
    # Orígenes de validación previos al holdout final: 4 bloques disjuntos.
    train_end = len(df) - H
    origins = [train_end - 4 * H + k * H for k in range(4)]
    validation = []
    configs = [(w, penalty) for w in WINDOWS for penalty in REGULARIZATION]
    for w, penalty in configs:
        individual = []
        for end in origins:
            train = df.iloc[:end]
            test = df.iloc[end:end + H]
            predictions = forecast(train, test['date'], w, penalty)
            score = metrics(test['unidades'].to_numpy(dtype=float), predictions)
            individual.append(score['WAPE_pct'])
            validation.append({'ventana_dias':w, 'penalizacion':penalty,
                               'inicio_validacion':str(test['date'].iloc[0].date()),
                               'WAPE_pct':score['WAPE_pct']})
        # Preferir menor error medio de los cuatro bloques de validación.
    summary_cv = (pd.DataFrame(validation).groupby(['ventana_dias', 'penalizacion'], as_index=False)
                  .agg(WAPE_validacion_promedio_pct=('WAPE_pct', 'mean'))
                  .sort_values('WAPE_validacion_promedio_pct', kind='stable'))
    winner = summary_cv.iloc[0]
    w, penalty = int(winner['ventana_dias']), float(winner['penalizacion'])
    train, test = df.iloc[:train_end], df.iloc[train_end:]
    y = test['unidades'].to_numpy(dtype=float)
    predictions = {'Dia_semana_8s': baseline(train, test['date']),
                   'Tendencia_semanal': forecast(train, test['date'], w, penalty)}
    results = pd.DataFrame([{'modelo':name, **metrics(y, p)} for name, p in predictions.items()])
    results = results.sort_values('WAPE_pct')
    comparison = pd.DataFrame({'date':test['date'], 'real':y.astype(int)})
    for name, p in predictions.items():
        comparison[name] = np.rint(p).astype(int)
    pd.DataFrame(validation).to_csv(OUT / 'validacion_temporal_tendencia.csv', index=False, encoding='utf-8-sig')
    summary_cv.to_csv(OUT / 'seleccion_modelo_tendencia.csv', index=False, encoding='utf-8-sig')
    comparison.to_csv(OUT / 'comparacion_tendencia_28d.csv', index=False, encoding='utf-8-sig')
    results.to_csv(OUT / 'metricas_tendencia_28d.csv', index=False, encoding='utf-8-sig')
    meta = {'periodo_prueba': [str(test['date'].iloc[0].date()), str(test['date'].iloc[-1].date())],
            'horizonte_dias':H,
            'modelo_seleccionado_en_validacion': {'ventana_dias':w,'penalizacion':penalty},
            'metricas_prueba': results.to_dict(orient='records'),
            'nota': 'Modelo agregado, sin stock real. Una sola prueba final de 28 días. La validación temporal selecciona los parámetros antes del holdout.'}
    (OUT / 'resumen_tendencia_28d.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(test['date'], y, label='Real', linewidth=2, color='black')
    for name, p in predictions.items():
        ax.plot(test['date'], p, label=name)
    ax.set(title='Caso 03 - baseline vs tendencia semanal (28 días)', xlabel='Fecha', ylabel='Unidades')
    ax.grid(alpha=.2)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(FIG / '04_tendencia_vs_baseline_28d.png', dpi=160)
    plt.close(fig)
    print('Validación temporal: 4 ventanas de 28 días, anteriores al período de prueba.')
    print('Parámetros seleccionados:', {'ventana_dias':w, 'penalizacion':penalty})
    print('PERIODO DE PRUEBA:', test['date'].iloc[0].date(), 'a', test['date'].iloc[-1].date())
    print(results.to_string(index=False, float_format=lambda n:f'{n:,.2f}'))
    print('\nArchivos creados:')
    for path in ['resultados/validacion_temporal_tendencia.csv',
                 'resultados/seleccion_modelo_tendencia.csv',
                 'resultados/comparacion_tendencia_28d.csv',
                 'resultados/metricas_tendencia_28d.csv',
                 'resultados/resumen_tendencia_28d.json',
                 'visualizaciones/04_tendencia_vs_baseline_28d.png']:
        print(' -', path)

if __name__ == '__main__':
    main()
