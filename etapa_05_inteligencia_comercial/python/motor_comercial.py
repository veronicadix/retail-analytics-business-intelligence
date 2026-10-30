"""V17: reglas comerciales explicables, sin IA de pago ni escrituras en BQ/PG.

Ejecutar desde la raíz del proyecto: .venv\\Scripts\\python.exe etapa_05_inteligencia_comercial\\python\\motor_comercial.py --local
La extracción usa el script consolidado de V16, para mantener una única fuente de métricas.
"""
import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'etapa_04_claude_api' / 'python'))
from informe_comercial import load_metrics, enrich_products_from_postgres, number, pct_refunds, safe_markdown

# Umbrales configurables y explícitos; son reglas analíticas, no verdades de negocio.
REFUND_PREMIUM_POINTS = 1.0
CONCENTRATION_WARNING_PCT = 75.0


def build_rules(data):
    m = data['resumen']
    gross = float(m.get('ventas_brutas_gbp') or 0)
    refunds = abs(float(m.get('abonos_mercancia_gbp') or 0))
    net = float(m.get('ventas_netas_gbp') or 0)
    if gross <= 0: raise ValueError('Ventas brutas deben ser positivas para calcular tasas')
    general_rate = 100 * refunds / gross
    categories = data['abc']
    alerts=[]
    a=categories['A']; a_share=float(a['participacion_ventas_positivas_pct'])
    if a_share >= CONCENTRATION_WARNING_PCT:
        alerts.append({'id':'CONCENTRACION_A','severidad':'MEDIA',
          'evidencia':f"Categoría A: {a['productos']} productos; {a_share:.2f}% de ventas netas positivas (GBP {number(a['ventas_netas_gbp'])}).",
          'accion':'Priorizar análisis de disponibilidad y margen; no aumentar inventario automáticamente.',
          'limitacion':'La venta histórica no acredita margen, existencias actuales ni necesidad de reposición.'})
    for p in data['top_productos']:
        p_gross=float(p.get('ventas_brutas_gbp') or 0)
        if p_gross<=0: continue
        rate=100*abs(float(p.get('abonos_gbp') or 0))/p_gross
        if rate >= general_rate + REFUND_PREMIUM_POINTS:
            alerts.append({'id':f"ABONOS_{p['producto']}", 'severidad':'REVISAR',
              'evidencia':f"{p.get('descripcion') or p['producto']} ({p['producto']}): tasa {rate:.2f}%, frente al {general_rate:.2f}% global; diferencia {rate-general_rate:.2f} puntos porcentuales.",
              'accion':'Examinar causas de abonos y volumen de transacciones antes de intervenir.',
              'limitacion':'Las tasas no demuestran defectos, causalidad ni cambios en la demanda.'})
    start=str(m.get('fecha_minima') or '')
    finish=str(m.get('fecha_maxima') or '')
    if finish.startswith('2011-12-09'):
        alerts.append({'id':'PERIODO_PARCIAL','severidad':'METODOLOGIA',
          'evidencia':f'Cobertura temporal: {start} a {finish}; diciembre de 2011 es parcial.',
          'accion':'Excluir diciembre de 2011 de comparaciones mensuales completas.',
          'limitacion':'No extrapolar resultados históricos como si fueran vigentes.'})
    if data.get('productos_sin_coincidencia'):
        alerts.append({'id':'CODIGOS_SIN_MAPEO','severidad':'CALIDAD',
          'evidencia':'Códigos sin coincidencia: '+', '.join(data['productos_sin_coincidencia']),
          'accion':'Revisar normalización del catálogo antes de interpretar esos productos.',
          'limitacion':'La ausencia de código puede deberse a diferencias de granularidad.'})
    if data.get('codigos_con_multiples_filas',0):
        alerts.append({'id':'GRANULARIDAD','severidad':'CALIDAD',
          'evidencia':f"{data['codigos_con_multiples_filas']} filas adicionales por código consolidado en PostgreSQL.",
          'accion':'Conservar el agrupamiento por código; revisar descripciones alternativas al auditar el catálogo.',
          'limitacion':'El número corresponde a filas adicionales, no a número de códigos duplicados.'})
    base=float(data['abc_total_positivo_gbp'])
    difference=base-net
    metrics={'ventas_netas_gbp':net,'ventas_brutas_gbp':gross,'abonos_gbp':-refunds,
             'tasa_abonos_pct':round(general_rate,4), 'base_abc_positiva_gbp':base,
             'diferencia_base_abc_vs_neto_gbp':round(difference,2),
             'productos_abc':sum(int(categories[c]['productos']) for c in ('A','B','C'))}
    return {'version':'V17','fecha_generacion_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'fuentes':[data['fuente'],data['fuente_catalogo_abc']],
            'metricas':metrics,'alertas':alerts,'top_productos':data['top_productos'],
            'abc':categories,'controles':{'filas_adicionales_consolidadas':data.get('codigos_con_multiples_filas',0),
            'codigos_sin_coincidencia':data.get('productos_sin_coincidencia',[])}}


def report_markdown(analysis):
    m=analysis['metricas']; alerts=analysis['alertas']; top=analysis['top_productos']
    lines=['# Informe ejecutivo de inteligencia comercial — V17','',
      f"**Generado UTC:** {analysis['fecha_generacion_utc']}",
      '**Fuente:** BigQuery (indicadores) + PostgreSQL (descripciones y Pareto/ABC por código).',
      '**Alcance:** datos históricos de 2009–2011, no representan la demanda actual.','',
      '## Indicadores verificables','',
      f"- Ventas netas: GBP {number(m['ventas_netas_gbp'])}",
      f"- Ventas brutas: GBP {number(m['ventas_brutas_gbp'])}",
      f"- Abonos: GBP {number(m['abonos_gbp'])} ({m['tasa_abonos_pct']:.2f}% de las ventas brutas)",
      f"- Catálogo Pareto: {m['productos_abc']:,} códigos de neto positivo.",
      f"- Denominador ABC positivo: GBP {number(m['base_abc_positiva_gbp'])}; diferencia con ventas netas globales: GBP {number(m['diferencia_base_abc_vs_neto_gbp'])}.",
      '', '## Distribución ABC (códigos únicos)','',
      '| Categoría | Productos | Ventas netas positivas GBP | % sobre base ABC |',
      '|:---:|---:|---:|---:|']
    for c in ('A','B','C'):
        a=analysis['abc'][c]; lines.append(f"| {c} | {a['productos']:,} | {number(a['ventas_netas_gbp'])} | {a['participacion_ventas_positivas_pct']:.2f}% |")
    lines += ['', '## Top 10 productos por ventas netas (BigQuery)', '',
       '| Código | Descripción PostgreSQL | Ventas netas GBP | Tasa abonos | ABC |',
       '|---|---|---:|---:|:---:|']
    for p in top:
        lines.append('| '+' | '.join([safe_markdown(p['producto']),safe_markdown(p.get('descripcion','Sin descripción')),
            number(p['ventas_netas_gbp']),pct_refunds(p.get('ventas_netas_gbp'),p.get('ventas_brutas_gbp'),p.get('abonos_gbp')),
            safe_markdown(p.get('categoria_abc','N/D'))])+' |')
    lines += ['', '## Alertas y recomendaciones generadas por reglas', '']
    if not alerts: lines.append('Ninguna regla disparó una alerta; esto no equivale a ausencia de riesgos.')
    for i,a in enumerate(alerts,1):
        lines += [f"### {i}. {a['id']} — {a['severidad']}", '',f"- **Evidencia:** {a['evidencia']}",
                  f"- **Acción sugerida:** {a['accion']}",f"- **Límite de interpretación:** {a['limitacion']}",'']
    lines += ['## Metodología y controles','',
      '- Las alertas usan reglas deterministas con umbrales publicados en el código; no son predicciones ni decisiones automáticas.',
      '- El cálculo ABC agrupa por código único y utiliza únicamente netos positivos de la vista PostgreSQL.',
      '- La tasa de abonos divide el valor absoluto de los abonos entre las ventas brutas (si son positivas).',
      f"- Filas adicionales consolidadas por código: {analysis['controles']['filas_adicionales_consolidadas']}.",
      '- Los nombres provienen de PostgreSQL, mientras que los importes del Top 10 provienen de BigQuery.',
      '- Las cifras se redondean para exhibición; contrastes y umbrales se calculan sin redondear.',
      '- No se consultan ni envían datos personales; no se ejecuta Claude API.', '']
    return '\n'.join(lines)


def save_reports(analysis,out):
    out.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    stem='inteligencia_comercial_'+stamp
    md=out/(stem+'.md'); js=out/(stem+'.json'); csv_path=out/(stem+'_alertas.csv')
    md.write_text(report_markdown(analysis),encoding='utf-8')
    js.write_text(json.dumps(analysis,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    with csv_path.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['id','severidad','evidencia','accion','limitacion']);writer.writeheader();writer.writerows(analysis['alertas'])
    return md,js,csv_path


def main():
    ap=argparse.ArgumentParser(description='V17 inteligencia comercial basada en reglas')
    ap.add_argument('--local',action='store_true',help='Sin Claude API; solo consultas read-only')
    args=ap.parse_args()
    print('Consultando métricas agregadas BigQuery y Pareto PostgreSQL (solo lectura)...',flush=True)
    data=enrich_products_from_postgres(load_metrics())
    result=build_rules(data)
    files=save_reports(result,ROOT/'etapa_05_inteligencia_comercial'/'salidas')
    for path in files:print('Generado:',path)
    print(f"Alertas: {len(result['alertas'])} | sin Claude API | no se modificaron datos")

if __name__=='__main__': main()
