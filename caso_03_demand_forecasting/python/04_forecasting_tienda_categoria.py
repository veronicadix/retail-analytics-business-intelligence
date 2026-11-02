"""Caso 03 - Pronostico por tienda/categoria M5 (28 dias).

Ejecutar desde la raiz del caso:
    python python/04_forecasting_tienda_categoria.py

Usa SOLO sales_train_validation.csv y calendar.csv del directorio datos/raw.
Reserva los ultimos 28 dias (2016-03-28 a 2016-04-24) para prueba.
Pronosticos independientes para cada combinacion tienda/categoria.
No hay datos de inventario real ni ventas futuras usadas para entrenar.
Dependencias: pandas, numpy, matplotlib.
"""
from pathlib import Path
import csv
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'datos' / 'raw'
OUT = ROOT / 'resultados'
FIG = ROOT / 'visualizaciones'
H = 28
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def pronosticos(train, dates):
    """Dos metodos para horizonte fijo, sin utilizar observaciones de prueba."""
    recent = train.tail(56)
    means = recent.groupby(recent.index.day_of_week).mean().reindex(range(7))
    weekday = np.array([means.iloc[d.day_of_week] for d in dates], dtype=float)
    last7 = train.tail(7).to_numpy(dtype=float)
    naive = np.resize(last7, len(dates))
    return {'Dia_semana_8s': np.maximum(0, weekday), 'Naive_7': np.maximum(0, naive)}


def metricas(real, pron):
    dif = pron - real
    total = float(real.sum())
    return {'MAE': float(np.mean(np.abs(dif))),
            'WAPE_pct': float(100 * np.abs(dif).sum() / total) if total else None,
            'Sesgo_pct': float(100 * dif.sum() / total) if total else None,
            'Unidades_reales': int(total),
            'Unidades_pronosticadas': float(pron.sum())}


def main():
    path = RAW / 'sales_train_validation.csv'
    calendar_path = RAW / 'calendar.csv'
    if not path.is_file() or not calendar_path.is_file():
        raise FileNotFoundError('Faltan sales_train_validation.csv o calendar.csv en datos/raw')

    with path.open(encoding='utf-8-sig', newline='') as f:
        columns = next(csv.reader(f))
    days = [c for c in columns if c.startswith('d_')]
    if len(days) <= H + 56:
        raise ValueError('El histórico no permite entrenar y probar 28 días.')
    cal = pd.read_csv(calendar_path, usecols=['d', 'date'], parse_dates=['date'])
    dates = pd.DatetimeIndex(cal.set_index('d').loc[days, 'date'])
    if dates.isna().any():
        raise ValueError('Hay días sin correspondencia en calendar.csv.')
    if not (dates[1:] - dates[:-1] == pd.Timedelta(days=1)).all():
        raise ValueError('El calendario no tiene días consecutivos.')

    print('[1/3] Agregando unidades por tienda y categoría en bloques...')
    groups = {}
    use = ['store_id', 'cat_id'] + days
    count = 0
    for chunk in pd.read_csv(path, usecols=use, chunksize=350,
                             dtype={d: 'int16' for d in days}):
        count += len(chunk)
        for (store, cat), group in chunk.groupby(['store_id', 'cat_id'], sort=False):
            arr = group[days].to_numpy(dtype=np.int64).sum(axis=0)
            key = (store, cat)
            if key in groups:
                groups[key] += arr
            else:
                groups[key] = arr
    print(f'    {count:,} series producto-tienda; {len(groups)} combinaciones tienda/categoría')

    print('[2/3] Evaluando pronósticos sobre los últimos 28 días...')
    train_dates, test_dates = dates[:-H], dates[-H:]
    rows, predictions = [], []
    for (store, cat), vals in sorted(groups.items()):
        train = pd.Series(vals[:-H], index=train_dates)
        real = vals[-H:].astype(float)
        for model, pred in pronosticos(train, test_dates).items():
            rows.append({'tienda': store, 'categoria': cat, 'modelo': model,
                         **metricas(real, pred)})
            for date, actual, expected in zip(test_dates, real, pred):
                predictions.append({'fecha': date.date().isoformat(), 'tienda': store,
                                    'categoria': cat, 'modelo': model,
                                    'unidades_reales': int(actual),
                                    'unidades_pronosticadas': round(float(expected), 3)})

    metrics_df = pd.DataFrame(rows)
    preds_df = pd.DataFrame(predictions)
    # Las métricas globales son micro-agregadas a partir de las 30 series, no la media simple de WAPEs.
    totals = []
    for model, group in preds_df.groupby('modelo'):
        real = group['unidades_reales'].to_numpy(dtype=float)
        pred = group['unidades_pronosticadas'].to_numpy(dtype=float)
        totals.append({'modelo': model, **metricas(real, pred)})
    global_df = pd.DataFrame(totals).sort_values('WAPE_pct')
    best = global_df.iloc[0]['modelo']
    winners = (metrics_df.sort_values(['tienda', 'categoria', 'WAPE_pct'], na_position='last')
               .drop_duplicates(['tienda', 'categoria']))

    metrics_df.to_csv(OUT / 'metricas_tienda_categoria_28d.csv', index=False, encoding='utf-8-sig')
    preds_df.to_csv(OUT / 'pronosticos_tienda_categoria_28d.csv', index=False, encoding='utf-8-sig')
    global_df.to_csv(OUT / 'metricas_globales_segmentadas_28d.csv', index=False, encoding='utf-8-sig')
    winners.to_csv(OUT / 'mejor_modelo_por_tienda_categoria.csv', index=False, encoding='utf-8-sig')
    summary = {
        'periodo_prueba': [test_dates[0].date().isoformat(), test_dates[-1].date().isoformat()],
        'horizonte_dias': H, 'numero_series_tienda_categoria': len(groups),
        'mejor_modelo_global_segmentado_por_WAPE': best,
        'metricas_globales_segmentadas': global_df.to_dict(orient='records'),
        'nota': ('Se pronostica cada tienda-categoria por separado. El WAPE global suma errores absolutos '
                 'por segmento, por lo que no es directamente comparable con el WAPE de la demanda '
                 'agregada. El mejor modelo por segmento es descriptivo del test, no una politica '
                 'validada para elegir modelos en el futuro.')}
    (OUT / 'resumen_tienda_categoria_28d.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    # Grafico para el modelo con menor WAPE global a nivel segmento.
    best_data = metrics_df[metrics_df['modelo'] == best].copy()
    best_data['segmento'] = best_data['tienda'] + ' / ' + best_data['categoria']
    best_data = best_data.sort_values('WAPE_pct', ascending=True)
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.barh(best_data['segmento'], best_data['WAPE_pct'])
    ax.invert_yaxis()
    ax.set(title=f'Caso 03 · WAPE por tienda y categoría ({best})',
           xlabel='WAPE (%)', ylabel='Segmento')
    ax.grid(axis='x', alpha=.2)
    fig.tight_layout()
    fig.savefig(FIG / '05_wape_tienda_categoria_28d.png', dpi=150)
    plt.close(fig)

    print('PERIODO DE PRUEBA:', test_dates[0].date(), 'a', test_dates[-1].date())
    print('\nMÉTRICAS GLOBALES DE PRONÓSTICOS SEGMENTADOS:')
    print(global_df[['modelo', 'MAE', 'WAPE_pct', 'Sesgo_pct']].to_string(index=False,
          float_format=lambda v: f'{v:,.2f}'))
    print('\nMejor modelo global por WAPE segmentado:', best)
    print('\n5 segmentos con mayor WAPE de ese modelo:')
    print(best_data.nlargest(5, 'WAPE_pct')[['tienda', 'categoria', 'WAPE_pct']]
          .to_string(index=False, float_format=lambda v: f'{v:,.2f}'))
    print('\nArchivos creados:')
    for name in ['metricas_tienda_categoria_28d.csv', 'pronosticos_tienda_categoria_28d.csv',
                 'metricas_globales_segmentadas_28d.csv', 'mejor_modelo_por_tienda_categoria.csv',
                 'resumen_tienda_categoria_28d.json']:
        print(' - resultados/' + name)
    print(' - visualizaciones/05_wape_tienda_categoria_28d.png')


if __name__ == '__main__':
    main()
