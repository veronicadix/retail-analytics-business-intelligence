"""Caso 05: carga completa verificada PostgreSQL -> BigQuery.

Uso: python python/03_pipeline_postgresql_bigquery.py
Requisitos: pip install -r requirements.txt; ADC de Google; variables en .env.

La carga usa tablas temporales en un dataset EXCLUSIVO del caso 05 y solo
promueve cada tabla al destino después de validar conteo y unicidad.
No proporciona atomicidad entre las tres tablas.
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
import time
import uuid
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
DATASET = 'retail_pipeline_case05'
LOCATION = 'US'
BATCH_SIZE = 50_000

TABLES = {
    'base_movimientos': {
        'key': 'id_linea',
        'fields': [
            ('id_linea', 'STRING', 'REQUIRED'), ('hoja_origen', 'STRING', 'NULLABLE'),
            ('fila_excel', 'INTEGER', 'NULLABLE'), ('factura', 'STRING', 'NULLABLE'),
            ('producto', 'STRING', 'NULLABLE'), ('descripcion', 'STRING', 'NULLABLE'),
            ('cantidad', 'NUMERIC', 'NULLABLE'), ('fecha', 'DATETIME', 'NULLABLE'),
            ('precio_gbp', 'NUMERIC', 'NULLABLE'), ('cliente_id', 'STRING', 'NULLABLE'),
            ('pais', 'STRING', 'NULLABLE'), ('importe_gbp', 'NUMERIC', 'NULLABLE'),
            ('clase_codigo', 'STRING', 'NULLABLE'), ('tipo_movimiento', 'STRING', 'NULLABLE'),
            ('incluir_ventas_brutas', 'INTEGER', 'NULLABLE'),
            ('incluir_abonos_mercancia', 'INTEGER', 'NULLABLE'),
            ('incluir_recompra', 'INTEGER', 'NULLABLE'),
            ('incluir_demanda_unidades', 'INTEGER', 'NULLABLE'),
            ('motivo_alcance', 'STRING', 'NULLABLE'),
        ],
    },
    'catalogo_codigos': {
        'key': 'producto',
        'fields': [
            ('producto', 'STRING', 'REQUIRED'), ('clase_codigo', 'STRING', 'NULLABLE'),
            ('descripcion_referencia', 'STRING', 'NULLABLE'),
            ('variantes_descripcion_en_ventas', 'INTEGER', 'NULLABLE'),
            ('filas_conservadas', 'INTEGER', 'NULLABLE'),
            ('lineas_venta', 'INTEGER', 'NULLABLE'), ('regla_origen', 'STRING', 'NULLABLE'),
        ],
    },
    'facturas_venta': {
        'key': 'factura',
        'fields': [
            ('factura', 'STRING', 'REQUIRED'), ('cliente_id', 'STRING', 'NULLABLE'),
            ('pais', 'STRING', 'NULLABLE'), ('fecha_factura', 'DATETIME', 'NULLABLE'),
            ('ultima_fecha_linea', 'DATETIME', 'NULLABLE'),
            ('flag_varias_horas', 'INTEGER', 'NULLABLE'),
            ('lineas_mercancia', 'INTEGER', 'NULLABLE'),
            ('unidades_mercancia', 'NUMERIC', 'NULLABLE'),
            ('importe_bruto_mercancia_gbp', 'NUMERIC', 'NULLABLE'),
            ('incluir_recompra', 'INTEGER', 'NULLABLE'),
        ],
    },
}


def needed_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise ValueError(f'Falta configurar {key} en el archivo .env')
    return val


def encode(value):
    if isinstance(value, Decimal):
        return str(value)  # preserva precisión NUMERIC
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def write_jsonl(conn: psycopg.Connection, table: str, fields: list, target: Path) -> int:
    columns = ', '.join('"' + f[0] + '"' for f in fields)
    count = 0
    with conn.cursor(name=f'cursor_{table}', row_factory=psycopg.rows.dict_row) as cur:
        cur.itersize = BATCH_SIZE
        cur.execute(f'SELECT {columns} FROM public."{table}"')
        with target.open('w', encoding='utf-8', newline='\n') as fp:
            while True:
                rows = cur.fetchmany(BATCH_SIZE)
                if not rows:
                    break
                for row in rows:
                    fp.write(json.dumps({k: encode(v) for k, v in row.items()}, ensure_ascii=False, allow_nan=False) + '\n')
                count += len(rows)
                logging.info('%s: extraídas %s filas', table, f'{count:,}')
    return count


def bq_scalar(client: bigquery.Client, sql: str, params=None) -> int:
    job_config = bigquery.QueryJobConfig(query_parameters=params or [])
    return int(next(iter(client.query(sql, job_config=job_config, location=LOCATION).result()))[0])


def run():
    ROOT.joinpath('resultados').mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    project = needed_env('GCP_PROJECT_ID')
    client = bigquery.Client(project=project)
    dataset_id = f'{project}.{DATASET}'
    try:
        ds = client.get_dataset(dataset_id)
        if ds.location.lower() != LOCATION.lower():
            raise ValueError(f'Dataset {dataset_id} está en {ds.location}; se esperaba {LOCATION}')
    except Exception as exc:
        from google.api_core.exceptions import NotFound
        if not isinstance(exc, NotFound):
            raise
        ds = bigquery.Dataset(dataset_id)
        ds.location = LOCATION
        client.create_dataset(ds)
        logging.info('Dataset creado: %s (%s)', dataset_id, LOCATION)

    params = {
        'host': os.getenv('PG_HOST', 'localhost'),
        'port': int(os.getenv('PG_PORT', '5432')),
        'dbname': os.getenv('PG_DATABASE', 'portafolio_retail'),
        'user': needed_env('PG_USER'),
        'password': needed_env('PG_PASSWORD'),
        'connect_timeout': 15,
    }
    summary = []
    with psycopg.connect(**params) as conn:
        # Consistencia de snapshot entre conteo y extracción de una tabla.
        for table, spec in TABLES.items():
            conn.rollback()  # nueva transacción por tabla
            conn.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY')
            start = time.monotonic()
            expected = int(conn.execute(f'SELECT COUNT(*) FROM public."{table}"').fetchone()[0])
            stage = f'{dataset_id}._stage_{table}_{uuid.uuid4().hex[:10]}'
            final = f'{dataset_id}.{table}'
            logging.info('Inicio: %s; filas origen=%s', table, f'{expected:,}')
            stage_created = False
            with tempfile.TemporaryDirectory(prefix='case05_') as tmpdir:
                path = Path(tmpdir) / f'{table}.jsonl'
                count = write_jsonl(conn, table, spec['fields'], path)
                if count != expected:
                    raise RuntimeError(f'{table}: extracción {count} != origen {expected}')
                schema = [bigquery.SchemaField(name, dtype, mode=mode)
                          for name, dtype, mode in spec['fields']]
                config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                    schema=schema,
                    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                    create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
                    max_bad_records=0,
                )
                try:
                    with path.open('rb') as stream:
                        client.load_table_from_file(stream, stage, job_config=config, location=LOCATION).result()
                    stage_created = True
                    key = spec['key']
                    check = client.query(
                        f'''SELECT COUNT(*) AS total, COUNTIF(`{key}` IS NULL) AS nulos,
                            COUNT(DISTINCT `{key}`) AS distintos FROM `{stage}`''',
                        location=LOCATION,
                    ).result()
                    total, nulos, distintos = tuple(next(iter(check)))
                    if int(total) != expected or int(nulos) != 0 or int(distintos) != expected:
                        raise RuntimeError(f'{table}: validación falló: filas={total}, claves nulas={nulos}, claves distintas={distintos}, esperado={expected}')
                    copy_conf = bigquery.CopyJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
                    client.copy_table(stage, final, job_config=copy_conf, location=LOCATION).result()
                    final_count = bq_scalar(client, f'SELECT COUNT(*) FROM `{final}`')
                    if final_count != expected:
                        raise RuntimeError(f'{table}: destino={final_count} != origen={expected}')
                    summary.append({'tabla': table, 'registros_origen': expected,
                                    'registros_bigquery': final_count, 'estado': 'OK',
                                    'segundos': round(time.monotonic() - start, 1)})
                    logging.info('OK %s: %s filas verificadas', table, f'{final_count:,}')
                finally:
                    if stage_created:
                        client.delete_table(stage, not_found_ok=True)
    output = ROOT / 'resultados' / '03_conciliacion_postgresql_bigquery.json'
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    logging.info('Conciliación guardada en %s', output)
    logging.info('COMPLETADO: %s', summary)


if __name__ == '__main__':
    try:
        run()
    except Exception:
        logging.exception('Pipeline interrumpido; revisar error antes de reintentar.')
        raise SystemExit(1)
