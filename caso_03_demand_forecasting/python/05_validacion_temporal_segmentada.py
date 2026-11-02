"""Caso 03 | Validacion temporal por tienda y categoria.
Ejecutar: python python/05_validacion_temporal_segmentada.py
Compara Dia_semana_8s y Naive_7 en 4 ventanas previas de 28 dias,
y evalua por separado los ultimos 28 dias (test final sin seleccion).
No utiliza datos del test final para elegir modelo.
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
RAW, OUT, FIG = ROOT/'datos'/'raw', ROOT/'resultados', ROOT/'visualizaciones'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
H = 28


def predict(train, future_dates):
    last = train.iloc[-56:]
    weekday_means = last.groupby(last.index.day_of_week).mean().reindex(range(7))
    weekday = np.array([weekday_means.iloc[d.day_of_week] for d in future_dates], dtype=float)
    naive = np.tile(train.iloc[-7:].to_numpy(dtype=float), 4)
    return {'Dia_semana_8s': np.maximum(weekday, 0), 'Naive_7': np.maximum(naive, 0)}


def evaluate(actual, pred):
    err = pred - actual
    denom = actual.sum()
    return {'error_abs':float(np.abs(err).sum()), 'error_neto':float(err.sum()),
            'unidades_reales':float(denom), 'n_dias':len(actual),
            'MAE':float(np.abs(err).mean()),
            'WAPE_pct':float(100*np.abs(err).sum()/denom) if denom else None,
            'Sesgo_pct':float(100*err.sum()/denom) if denom else None}


def main():
    src = RAW/'sales_train_validation.csv'
    cal = RAW/'calendar.csv'
    if not src.exists() or not cal.exists():
        raise FileNotFoundError('Se requieren sales_train_validation.csv y calendar.csv en datos/raw')
    with src.open(encoding='utf-8-sig', newline='') as f:
        names = next(csv.reader(f))
    days = [v for v in names if v.startswith('d_')]
    calendar = pd.read_csv(cal, usecols=['d', 'date'], parse_dates=['date']).set_index('d')
    dates = pd.DatetimeIndex(calendar.loc[days, 'date'])
    groups = {}
    print('[1/3] Leyendo y agregando por tienda/categoria...')
    for chunk in pd.read_csv(src, usecols=['store_id','cat_id'] + days, chunksize=350,
                             dtype={d:'int16' for d in days}):
        for key, rows in chunk.groupby(['store_id','cat_id'], sort=False):
            totals = rows[days].to_numpy(dtype=np.int64).sum(axis=0)
            if key not in groups:
                groups[key] = totals
            else:
                groups[key] += totals
    # Four preceding validation windows and one untouched final test.
    # Validation: [-140:-112], [-112:-84], [-84:-56], [-56:-28]
    boundaries = [(len(days)-140+i*H,len(days)-112+i*H) for i in range(4)]
    boundaries.append((len(days)-H,len(days)))
    print('[2/3] Calculando validacion y test final...')
    records = []
    for (store, category), values in sorted(groups.items()):
        for fold, (a,b) in enumerate(boundaries):
            train = pd.Series(values[:a], index=dates[:a])
            actual = values[a:b].astype(float)
            for model, forecast in predict(train, dates[a:b]).items():
                records.append({'tienda':store,'categoria':category,
                                'particion':'test_final' if fold == 4 else 'validacion',
                                'ventana':fold+1,
                                'fecha_inicio':str(dates[a].date()),
                                'fecha_fin':str(dates[b-1].date()),
                                'modelo':model, **evaluate(actual,forecast)})
    df = pd.DataFrame(records)
    df.to_csv(OUT/'validacion_segmentada_ventanas.csv', index=False, encoding='utf-8-sig')
    # Choose per segment based strictly on pre-test validation micro WAPE.
    val = df[df.particion == 'validacion']
    agg = val.groupby(['tienda','categoria','modelo'], as_index=False)[
        ['error_abs','error_neto','unidades_reales','n_dias']].sum()
    agg['WAPE_validacion_pct'] = 100*agg.error_abs/agg.unidades_reales.replace(0,np.nan)
    winners = agg.sort_values(['tienda','categoria','WAPE_validacion_pct','modelo']).drop_duplicates(['tienda','categoria'])
    winners = winners[['tienda','categoria','modelo','WAPE_validacion_pct']].rename(columns={'modelo':'modelo_elegido'})
    winners.to_csv(OUT/'seleccion_segmentada_por_validacion.csv', index=False, encoding='utf-8-sig')
    test = df[df.particion == 'test_final'].merge(winners, on=['tienda','categoria'])
    test['politica'] = np.where(test.modelo == test.modelo_elegido, 'Seleccion_validacion', 'No_seleccionado')
    # Compare global common baselines vs validated selection.
    chosen = test[test.politica=='Seleccion_validacion']
    def summary(frame,label):
        err, real, net = frame.error_abs.sum(),frame.unidades_reales.sum(),frame.error_neto.sum()
        return {'politica':label,'WAPE_pct':100*err/real,'Sesgo_pct':100*net/real,
                'MAE':err/frame.n_dias.sum(), 'unidades_reales':real}
    comparison = pd.DataFrame([
        summary(test[test.modelo=='Dia_semana_8s'],'Dia_semana_8s'),
        summary(test[test.modelo=='Naive_7'],'Naive_7'),
        summary(chosen,'Seleccion_validacion')]).sort_values('WAPE_pct')
    comparison.to_csv(OUT/'comparacion_validacion_segmentada_28d.csv', index=False, encoding='utf-8-sig')
    (OUT/'resumen_validacion_segmentada.json').write_text(json.dumps({
        'metodo':'4 ventanas de validacion de 28 dias, seguidas de test final independiente de 28 dias',
        'validacion_periodos':[{'inicio':str(dates[a].date()),'fin':str(dates[b-1].date())} for a,b in boundaries[:4]],
        'test_final':{'inicio':str(dates[boundaries[-1][0]].date()),'fin':str(dates[-1].date())},
        'eleccion_por_validacion':winners.modelo_elegido.value_counts().to_dict(),
        'resultados_test_final':comparison.to_dict('records'),
        'advertencia':'Seleccionar sobre validacion no garantiza superar baseline en test final.'
    }, ensure_ascii=False, indent=2),encoding='utf-8')
    fig,ax=plt.subplots(figsize=(9,4.5))
    ax.barh(comparison.politica, comparison.WAPE_pct)
    ax.invert_yaxis();ax.set_xlabel('WAPE de test final (%)');ax.set_title('Validacion temporal: estrategias segmentadas')
    ax.grid(axis='x',alpha=.2);fig.tight_layout()
    fig.savefig(FIG/'06_validacion_temporal_segmentada.png',dpi=150);plt.close(fig)
    print('\n[3/3] RESULTADO TEST FINAL:')
    print(comparison[['politica','MAE','WAPE_pct','Sesgo_pct']].to_string(index=False,float_format=lambda v:f'{v:,.2f}'))
    print('\nEleccion por validacion:')
    print(winners.modelo_elegido.value_counts().to_string())
    print('\nArchivos generados en resultados/: validacion_segmentada_ventanas.csv,')
    print(' seleccion_segmentada_por_validacion.csv, comparacion_validacion_segmentada_28d.csv,')
    print(' resumen_validacion_segmentada.json')
    print('Visualizacion: visualizaciones/06_validacion_temporal_segmentada.png')

if __name__=='__main__':
    main()
