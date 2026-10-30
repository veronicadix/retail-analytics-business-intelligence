"""V18: convierte el JSON verificable de V17 en tablas planas para Power BI.

Sin consultas ni gastos: python exportar_powerbi.py --from-json RUTA_ARCHIVO.json
Actualización opcional: python exportar_powerbi.py --live
Los resultados se excluyen de GitHub; no usa Claude ni edita archivos .pbix.
"""
import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'etapa_06_powerbi_portafolio' / 'salidas'


def csv_file(name, fields, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    return p


def numeric(x):
    return float(x or 0)


def export(analysis):
    # Contrato exacto del JSON generado por V17: metricas, abc, top_productos, alertas, controles.
    for field in ('metricas', 'abc', 'top_productos', 'alertas', 'controles'):
        if field not in analysis:
            raise ValueError(f'Falta la clave requerida en JSON V17: {field}')
    if not isinstance(analysis['alertas'], list) or not isinstance(analysis['top_productos'], list):
        raise ValueError('Las claves alertas y top_productos deben ser listas')
    generation = analysis.get('fecha_generacion_utc', '')
    metrics = analysis['metricas']
    kpis = [{'indicador': label, 'valor': numeric(metrics.get(key)), 'unidad': unit,
             'fuente_generacion_utc': generation}
            for key, label, unit in [
                ('ventas_brutas_gbp', 'Ventas brutas', 'GBP'),
                ('ventas_netas_gbp', 'Ventas netas', 'GBP'),
                ('abonos_gbp', 'Abonos de mercancía', 'GBP'),
                ('tasa_abonos_pct', 'Tasa de abonos', '%'),
                ('productos_abc', 'Productos ABC con neto positivo', 'códigos'),
                ('base_abc_positiva_gbp', 'Base Pareto positiva', 'GBP'),
                ('diferencia_base_abc_vs_neto_gbp', 'Diferencia base ABC vs neto', 'GBP')]]
    # No convertir estados en rankings: son etiquetas operativas de V17.
    alerts = []
    for idx, a in enumerate(analysis['alertas'], 1):
        alerts.append({'orden': idx, 'id_alerta': a['id'], 'severidad': a['severidad'],
                       'evidencia': a['evidencia'], 'accion_sugerida': a['accion'],
                       'limitacion': a['limitacion'],
                       'codigo_producto': a['id'].removeprefix('ABONOS_') if a['id'].startswith('ABONOS_') else '',
                       'fecha_generacion_utc': generation})
    abc = [{'categoria_abc': cat,
            'cantidad_productos': int(analysis['abc'][cat]['productos']),
            'ventas_netas_positivas_gbp': numeric(analysis['abc'][cat]['ventas_netas_gbp']),
            'participacion_pct': numeric(analysis['abc'][cat]['participacion_ventas_positivas_pct'])}
           for cat in ('A', 'B', 'C')]
    products = []
    for ix, p in enumerate(analysis['top_productos'], 1):
        gross = numeric(p.get('ventas_brutas_gbp'))
        refund = numeric(p.get('abonos_gbp'))
        products.append({'ranking': ix, 'codigo_producto': str(p['producto']),
                         'descripcion': p.get('descripcion', '') or 'Sin descripción',
                         'categoria_abc': p.get('categoria_abc', 'N/D'),
                         'ventas_brutas_gbp': gross,
                         'ventas_netas_gbp': numeric(p.get('ventas_netas_gbp')),
                         'abonos_gbp': refund,
                         'tasa_abonos_pct': 100 * abs(refund) / gross if gross > 0 else 0})
    quality = [
        {'control': 'Filas adicionales consolidadas por código', 'valor': int(analysis['controles'].get('filas_adicionales_consolidadas', 0)), 'unidad': 'filas'},
        {'control': 'Códigos sin coincidencia', 'valor': len(analysis['controles'].get('codigos_sin_coincidencia', [])), 'unidad': 'códigos'},
        {'control': 'Diferencia base Pareto vs ventas netas', 'valor': numeric(metrics.get('diferencia_base_abc_vs_neto_gbp')), 'unidad': 'GBP'},
    ]
    output = [
        csv_file('v18_kpis.csv', list(kpis[0]), kpis),
        csv_file('v18_abc.csv', list(abc[0]), abc),
        csv_file('v18_top_productos.csv', list(products[0]) if products else ['ranking','codigo_producto','descripcion','categoria_abc','ventas_brutas_gbp','ventas_netas_gbp','abonos_gbp','tasa_abonos_pct'], products),
        csv_file('v18_alertas.csv', ['orden','id_alerta','severidad','evidencia','accion_sugerida','limitacion','codigo_producto','fecha_generacion_utc'], alerts),
        csv_file('v18_calidad.csv', list(quality[0]), quality),
    ]
    manifest = {'version':'V18','origen':'JSON V17 (o generación V17 --live)',
                'fecha_ejecucion_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
                'fecha_indicadores_utc':generation,'numero_alertas':len(alerts),
                'archivos':[p.name for p in output],
                'advertencias':['Histórico 2009-2011, no vigencia actual',
                               'Top productos solo contiene 10 filas; no confundir con catálogo completo',
                               'La base ABC incluye exclusivamente netos positivos',
                               'Alertas por reglas, no predicciones']}
    path=OUT/'v18_manifest.json';path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');output.append(path)
    return output


def main():
    ap=argparse.ArgumentParser(description='V18: exportar alertas/ABC V17 a CSV para Power BI')
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--from-json', type=Path, metavar='V17_JSON', help='Utiliza el JSON guardado por V17 sin consultar bases')
    mode.add_argument('--live', action='store_true', help='Ejecuta lectura de BigQuery + PostgreSQL para construir V17 en memoria')
    args=ap.parse_args()
    if args.from_json:
        analysis=json.loads(args.from_json.read_text(encoding='utf-8-sig'))
    else:
        sys.path.insert(0, str(ROOT/'etapa_05_inteligencia_comercial'/'python'))
        from motor_comercial import load_metrics, enrich_products_from_postgres, build_rules
        analysis=build_rules(enrich_products_from_postgres(load_metrics()))
    paths=export(analysis)
    print('Exportación V18 exitosa (sin cambiar PostgreSQL, BigQuery ni .pbix):')
    for p in paths:print('Generado:',p)
    print('Alertas:',len(analysis['alertas']),'| Fuente: V17 | Claude API: no usada')

if __name__=='__main__':main()
