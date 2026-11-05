"""Ejecuta la conciliación comercial de seis métricas en BigQuery (solo lectura)."""
from __future__ import annotations
import sys
import time
from pathlib import Path
from google.cloud import bigquery

EXPECTED = {'abonos_mercancia_gbp', 'lineas_totales', 'lineas_venta',
            'unidades_demanda', 'ventas_brutas_gbp', 'ventas_netas_gbp'}


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python 08_validar_metricas.py <ruta_SQL>')
    sql_file = Path(sys.argv[1])
    sql = sql_file.read_text(encoding='utf-8')
    client = bigquery.Client(project='maximal-arcade-512100-h2')
    for attempt in (1, 2):
        try:
            rows = [dict(r.items()) for r in client.query(sql, location='US').result()]
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3)
    if len(rows) != 6 or {r['metrica'] for r in rows} != EXPECTED:
        raise ValueError('Se esperaban seis métricas comerciales distintas')
    failed = [r['metrica'] for r in rows if r.get('estado') != 'OK' or r.get('diferencia') is None or r['diferencia'] != 0]
    if failed:
        raise ValueError(f'Métricas sin conciliar: {failed}')
    print('OK: 6/6 métricas conciliadas con diferencia 0')


if __name__ == '__main__':
    main()
