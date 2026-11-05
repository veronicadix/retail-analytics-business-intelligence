#!/usr/bin/env python3
"""Caso 05: IA sobre métricas conciliadas. Una única llamada opcional de bajo consumo."""
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / 'resultados' / '07_conciliacion_metricas_comerciales.csv'
OUT = ROOT / 'resultados'
EXPECTED = {'abonos_mercancia_gbp','lineas_totales','lineas_venta', 'unidades_demanda','ventas_brutas_gbp','ventas_netas_gbp'}
MODEL = 'claude-haiku-4-5-20251001'


def num(s):
    try:
        return Decimal(str(s).strip())
    except (InvalidOperation, ValueError):
        raise ValueError('Valor numérico inválido en CSV')


def read_metrics():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f'No existe {CSV_FILE}; exporta el resultado de la consulta SQL 07.')
    with CSV_FILE.open(encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != len(EXPECTED):
        raise ValueError(f'Se esperaban seis métricas, recibidas: {len(rows)}')
    result = {}
    for row in rows:
        key = row.get('metrica','').strip()
        if key not in EXPECTED or key in result:
            raise ValueError(f'Métrica desconocida o repetida: {key}')
        source, mart, difference = (num(row.get(x,'')) for x in ('valor_fuente','valor_mart','diferencia'))
        if row.get('estado','').strip().upper() != 'OK' or source != mart or difference != 0:
            raise ValueError(f'Conciliación no aprobada: {key}')
        result[key] = format(source, 'f')
    return result


def prompt_payload(metrics):
    return ('Estas métricas históricas de retail fueron calculadas y conciliadas en BigQuery. '
            'No describas cambios, tendencias, causas, crecimiento ni tasas: solo hay valores agregados. '
            'Propón hasta tres observaciones cualitativas y verificaciones razonables. '
            'Devuelve EXCLUSIVAMENTE JSON válido, como una lista de objetos con las claves '
            'metric_key, observacion, recomendacion, limitacion. '
            'metric_key debe ser una de las claves recibidas. No incluyas ningún dígito ni cantidades en los textos. '
            'No afirmes causalidades ni resultados de implementación. Datos: '
            +json.dumps(metrics, ensure_ascii=False))


def validate_insights(items):
    if not isinstance(items, list) or not 1 <= len(items) <= 3:
        raise ValueError('La respuesta debe tener entre una y tres observaciones')
    for item in items:
        if not isinstance(item, dict) or set(item) != {'metric_key','observacion','recomendacion','limitacion'}:
            raise ValueError('Estructura de respuesta inesperada')
        if item['metric_key'] not in EXPECTED:
            raise ValueError('La IA citó una métrica desconocida')
        for key in ('observacion','recomendacion','limitacion'):
            val=item[key]
            if not isinstance(val,str) or not val.strip() or re.search(r'\d',val):
                raise ValueError(f'Campo inválido o con cifras no verificadas: {key}')
    return items


def live_call(metrics):
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env')
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('Configura ANTHROPIC_API_KEY en el .env local; nunca la compartas.')
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError('Falta SDK: .venv\\Scripts\\python.exe -m pip install anthropic') from exc
    client = anthropic.Anthropic(api_key=api_key, max_retries=0, timeout=30.0)
    response=client.messages.create(
        model=MODEL,
        max_tokens=650,
        messages=[{'role':'user','content':prompt_payload(metrics)}],
    )
    if response.stop_reason != 'end_turn':
        raise ValueError(f'Respuesta incompleta de la API: {response.stop_reason}')
    raw=''.join(block.text for block in response.content if getattr(block,'type','')=='text').strip()
    # Accept JSON fenced response if provider included fences despite prompt.
    if raw.startswith('```'):
        raw=re.sub(r'^```(?:json)?\s*|\s*```$', '', raw).strip()
    insights=validate_insights(json.loads(raw))
    return insights, {'input_tokens':response.usage.input_tokens,'output_tokens':response.usage.output_tokens,'model':MODEL}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--live',action='store_true',help='Autoriza una llamada de pago a Anthropic')
    args=p.parse_args()
    metrics=read_metrics()
    print('OK: seis métricas conciliadas; diferencias cero.')
    if not args.live:
        print('MODO SIMULACIÓN: ninguna solicitud a Claude, costo cero.')
        print('Para generar el informe: python python\\09_insights_claude.py --live')
        return
    insights, usage=live_call(metrics)
    OUT.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    data={'fecha_utc':stamp,'fuente':'07_conciliacion_metricas_comerciales.csv',
          'metricas_validadas':metrics,'insights_propuestos_no_verificados':insights,'uso_api':usage}
    (OUT/f'09_insights_claude_{stamp}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# Caso 05 — Insights comerciales asistidos por IA','',
        '## Métricas validadas (fuente BigQuery)', '',
        '| Métrica | Valor |','|---|---:|']
    md += [f'| `{k}` | {v} |' for k,v in metrics.items()]
    md += ['', '## Observaciones generadas por Claude (hipótesis; requieren revisión humana)', '']
    for i,item in enumerate(insights,1):
        md += [f'### Observación {i}: `{item["metric_key"]}`',
               item['observacion'], '',f'**Recomendación propuesta:** {item["recomendacion"]}',
               '',f'**Limitación:** {item["limitacion"]}','']
    md += ['---','Los valores numéricos proceden exclusivamente del CSV conciliado; el texto IA no constituye evidencia causal.']
    (OUT/f'09_reporte_ia_{stamp}.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(f'OK: informe y JSON guardados en {OUT}; tokens entrada={usage["input_tokens"]}, salida={usage["output_tokens"]}.')

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        sys.exit(1)
