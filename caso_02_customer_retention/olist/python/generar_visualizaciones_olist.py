from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def detectar_ruta_olist() -> Path:
    base = Path.cwd()
    candidatos = [
        base,
        base.parent,
        base / 'olist',
        base.parent / 'olist',
        base.parent.parent / 'olist',
    ]
    for c in candidatos:
        if (c / 'resultados').exists() and (c / 'visualizaciones').exists():
            return c
    # fallback típico del repo
    return base


def formatear_miles(x, pos=None):
    return f"{int(x):,}".replace(',', '.')


def formatear_pct(x, pos=None):
    return f"{x:.0f}%"


def guardar_fig(fig, ruta: Path):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"OK -> {ruta}")


def cargar_csv(ruta: Path) -> pd.DataFrame:
    return pd.read_csv(ruta, encoding='utf-8-sig')


def grafico_recompra(df_ind: pd.DataFrame, outdir: Path):
    fila = df_ind.iloc[0]
    df = pd.DataFrame({
        'grupo': ['Una compra', 'Recurrentes'],
        'clientes': [fila['compradores_una_compra'], fila['compradores_recurrentes']]
    })
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(df['grupo'], df['clientes'])
    ax.set_title('Olist — Distribución de compradores por recompra')
    ax.set_xlabel('Número de compradores')
    ax.xaxis.set_major_formatter(FuncFormatter(formatear_miles))
    total = df['clientes'].sum()
    for bar, val in zip(bars, df['clientes']):
        pct = 100 * val / total
        ax.text(val, bar.get_y() + bar.get_height()/2,
                f' {formatear_miles(val)} ({pct:.2f}%)', va='center')
    ax.text(0.01, -0.18,
            f"Tasa de recompra observada: {fila['tasa_recompra_pct']:.2f}% | Compradores únicos: {formatear_miles(fila['compradores_unicos'])}",
            transform=ax.transAxes)
    guardar_fig(fig, outdir / '01_olist_recompra.png')


def grafico_retencion(df_ret: pd.DataFrame, outdir: Path):
    df = df_ret.copy()
    df['mes'] = df['mes_retencion'].apply(lambda x: f"M{x}")
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df['mes'], df['retencion_ponderada_pct'])
    ax.set_title('Olist — Retención ponderada por cohorte')
    ax.set_xlabel('Mes de retención exacta')
    ax.set_ylabel('Retención (%)')
    ax.set_ylim(0, max(df['retencion_ponderada_pct']) * 1.35)
    for bar, pct, cli, coh in zip(bars, df['retencion_ponderada_pct'], df['clientes_retenidos'], df['cohortes_analizadas']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{pct:.2f}%', ha='center', va='bottom')
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                f'{int(cli)}\nclientes', ha='center', va='center', fontsize=9)
    ax.text(0.01, -0.2,
            'Notas: M1, M3 y M6 utilizan cohortes elegibles diferentes y miden actividad en el mes exacto, no retención acumulada.',
            transform=ax.transAxes)
    guardar_fig(fig, outdir / '02_olist_retencion_ponderada.png')


def grafico_segmentos(df_seg: pd.DataFrame, outdir: Path):
    df = df_seg.sort_values('clientes', ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(df['segmento_cliente'], df['clientes'])
    ax.set_title('Olist — Segmentación de compradores')
    ax.set_xlabel('Clientes')
    ax.xaxis.set_major_formatter(FuncFormatter(formatear_miles))
    for bar, clientes, pct, valor in zip(bars, df['clientes'], df['porcentaje_clientes'], df['valor_historico_brl']):
        ax.text(clientes, bar.get_y() + bar.get_height()/2,
                f' {formatear_miles(clientes)} | {pct:.2f}% | R$ {valor:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                va='center', fontsize=9)
    ax.text(0.01, -0.18,
            'Segmentación exploratoria con umbral histórico de 90 días. No representa estado actual de los clientes.',
            transform=ax.transAxes)
    guardar_fig(fig, outdir / '03_olist_segmentos_clientes.png')


def grafico_comparacion_recompra(df_comp: pd.DataFrame, outdir: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df_comp['dataset'], df_comp['tasa_recompra_pct'])
    ax.set_title('Comparación — Tasa de recompra observada')
    ax.set_ylabel('Recompra (%)')
    ax.set_ylim(0, 100)
    for bar, val in zip(bars, df_comp['tasa_recompra_pct']):
        ax.text(bar.get_x() + bar.get_width()/2, val, f'{val:.2f}%', ha='center', va='bottom')
    ax.text(0.01, -0.22,
            'No combinar registros ni interpretar la diferencia como experimento controlado: ambos datasets tienen reglas y periodos distintos.',
            transform=ax.transAxes)
    guardar_fig(fig, outdir / '04_comparacion_recompra_datasets.png')


def grafico_comparacion_retencion(df_comp: pd.DataFrame, outdir: Path):
    meses = ['retencion_m1_pct', 'retencion_m3_pct', 'retencion_m6_pct']
    etiquetas = ['M1', 'M3', 'M6']
    x = range(len(etiquetas))
    width = 0.35

    olist = df_comp.loc[df_comp['dataset'] == 'Olist', meses].iloc[0].tolist()
    online = df_comp.loc[df_comp['dataset'] == 'Online Retail II', meses].iloc[0].tolist()

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar([i - width/2 for i in x], online, width, label='Online Retail II')
    bars2 = ax.bar([i + width/2 for i in x], olist, width, label='Olist')
    ax.set_title('Comparación — Retención mensual ponderada')
    ax.set_xticks(list(x))
    ax.set_xticklabels(etiquetas)
    ax.set_ylabel('Retención (%)')
    ax.legend()
    ymax = max(online + olist)
    ax.set_ylim(0, ymax * 1.25)
    for bars in [bars1, bars2]:
        for bar in bars:
            val = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, val, f'{val:.2f}%', ha='center', va='bottom', fontsize=9)
    ax.text(0.01, -0.2,
            'Las tasas M1, M3 y M6 son exactas por mes de seguimiento y usan cohortes elegibles diferentes.',
            transform=ax.transAxes)
    guardar_fig(fig, outdir / '05_comparacion_retencion_datasets.png')


def grafico_heatmap_cohortes(opcional_csv: Path, outdir: Path):
    if not opcional_csv.exists():
        print('Saltado heatmap: no existe 06_detalle_cohortes_olist.csv')
        return
    df = cargar_csv(opcional_csv)
    pivot = df.pivot(index='mes_cohorte', columns='mes_desde_primera_compra', values='retencion_pct').sort_index()
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(pivot.values, aspect='auto')
    ax.set_title('Olist — Heatmap de cohortes de retención')
    ax.set_xlabel('Mes desde primera compra')
    ax.set_ylabel('Mes cohorte')
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([str(x)[:7] for x in pivot.index])
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.iloc[i, j]
            if pd.notna(val):
                ax.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=7)
    fig.colorbar(im, ax=ax, label='Retención %')
    guardar_fig(fig, outdir / '06_olist_heatmap_cohortes.png')


def main():
    olist = detectar_ruta_olist()
    resultados = olist / 'resultados'
    visualizaciones = olist / 'visualizaciones'

    df_ind = cargar_csv(resultados / '01_indicadores_generales.csv')
    df_ret = cargar_csv(resultados / '02_retencion_ponderada.csv')
    df_seg = cargar_csv(resultados / '04_segmentos_clientes.csv')
    df_comp = cargar_csv(resultados / '05_comparacion_resumen.csv')

    grafico_recompra(df_ind, visualizaciones)
    grafico_retencion(df_ret, visualizaciones)
    grafico_segmentos(df_seg, visualizaciones)
    grafico_comparacion_recompra(df_comp, visualizaciones)
    grafico_comparacion_retencion(df_comp, visualizaciones)
    grafico_heatmap_cohortes(resultados / '06_detalle_cohortes_olist.csv', visualizaciones)

    print('\nProceso finalizado. Revisa la carpeta visualizaciones.')


if __name__ == '__main__':
    main()
