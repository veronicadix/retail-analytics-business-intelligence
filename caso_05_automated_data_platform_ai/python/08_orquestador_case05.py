"""Orquestador local Caso 05. Solo librerías estándar; comandos externos ya instalados.

Modo predeterminado `verify`: dbt run -> dbt test -> conciliación SQL.
Modo `full`: ETL PostgreSQL -> BigQuery + verificación JSON -> dbt run/test -> conciliación.
No hay reintentos automáticos de operaciones que escriben datos.
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DBT_DIR = ROOT / 'dbt'
RESULTS = ROOT / 'resultados'
LOGS = ROOT / 'logs'
EXPECTED = {'base_movimientos': 1_033_036, 'catalogo_codigos': 5_304, 'facturas_venta': 39_516}
PROJECT = 'maximal-arcade-512100-h2'
LOCATION = 'US'


def locate_dbt(value: str | None) -> str:
    if value:
        return value
    default = Path(r'C:\venvs\retail05_dbt\Scripts\dbt.exe')
    return str(default) if default.exists() else 'dbt'


def run_process(label: str, command: list[str], cwd: Path, log: logging.Logger):
    start = time.monotonic()
    log.info('INICIO %s', label)
    # No se imprime el comando: puede incluir opciones sensibles en futuras modificaciones.
    with subprocess.Popen(command, cwd=str(cwd), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                          errors='replace', bufsize=1) as process:
        assert process.stdout is not None
        for line in process.stdout:
            log.info('[%s] %s', label, line.rstrip())
        code = process.wait()
    elapsed = round(time.monotonic() - start, 2)
    if code != 0:
        raise RuntimeError(f'{label}: proceso terminó con código {code}; consulta el log')
    log.info('OK %s | %.2f segundos', label, elapsed)
    return {'paso': label, 'estado': 'OK', 'segundos': elapsed}


def validate_etl_json():
    path = RESULTS / '03_conciliacion_postgresql_bigquery.json'
    if not path.is_file():
        raise FileNotFoundError(f'No existe evidencia ETL: {path}')
    rows = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        raise ValueError('Conciliación ETL incompleta')
    actual = {r['tabla']: r for r in rows}
    if set(actual) != set(EXPECTED):
        raise ValueError(f'Tablas ETL inesperadas: {sorted(actual)}')
    for name, count in EXPECTED.items():
        r = actual[name]
        if r.get('estado') != 'OK' or int(r.get('registros_origen', -1)) != count or int(r.get('registros_bigquery', -1)) != count:
            raise ValueError(f'Conciliación ETL inválida: {name}')
    return {'paso': 'verificar_etl', 'estado': 'OK', 'tablas': len(actual), 'registros': sum(EXPECTED.values())}


def main():
    parser = argparse.ArgumentParser(description='Orquestador local Caso 05')
    parser.add_argument('--mode', choices=('verify', 'full'), default='verify',
                        help='verify (predeterminado): dbt+validación, full: incluye ETL que reescribe destino del Caso 05')
    parser.add_argument('--dbt-exe', help='Ruta a dbt.exe')
    parser.add_argument('--python-etl', help='Ruta a python.exe del entorno del ETL')
    args = parser.parse_args()
    RESULTS.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:6]
    logfile = LOGS / f'08_orquestacion_{run_id}.log'
    logger = logging.getLogger('case05')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    fmt = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    for handler in [logging.FileHandler(logfile, encoding='utf-8'), logging.StreamHandler(sys.stdout)]:
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    report = {'run_id': run_id, 'mode': args.mode, 'inicio_utc': datetime.now(timezone.utc).isoformat(),
              'estado': 'EN_PROCESO', 'pasos': [], 'log_local': str(logfile)}
    report_path = RESULTS / f'08_orquestacion_{run_id}.json'
    try:
        if not (DBT_DIR / 'dbt_project.yml').exists() or not (DBT_DIR / 'profiles.yml').exists():
            raise FileNotFoundError('Faltan dbt_project.yml o profiles.yml en la carpeta dbt')
        dbt = locate_dbt(args.dbt_exe)
        if args.mode == 'full':
            python_exe = args.python_etl or str(ROOT / '.venv' / 'Scripts' / 'python.exe')
            report['pasos'].append(run_process('etl', [python_exe, str(ROOT / 'python' / '03_pipeline_postgresql_bigquery.py')], ROOT, logger))
            report['pasos'].append(validate_etl_json())
        # Ejecutar dbt dentro del proyecto y con el perfil ya validado.
        report['pasos'].append(run_process('dbt_run', [dbt, 'run', '--profiles-dir', '.'], DBT_DIR, logger))
        report['pasos'].append(run_process('dbt_test', [dbt, 'test', '--profiles-dir', '.'], DBT_DIR, logger))
        sql = ROOT / 'sql' / '07_conciliacion_metricas_comerciales.sql'
        # BigQuery Python se importa desde el propio entorno de ETL, no desde dbt.
        # Subproceso específico con JSON, para no asumir google-cloud-bigquery instalado en el Python del sistema.
        python_exe = args.python_etl or str(ROOT / '.venv' / 'Scripts' / 'python.exe')
        check_script = ROOT / 'python' / '08_validar_metricas.py'
        report['pasos'].append(run_process('conciliar_metricas', [python_exe, str(check_script), str(sql)], ROOT, logger))
        report['estado'] = 'OK'
        logger.info('COMPLETADO: ejecución %s', run_id)
    except Exception as exc:
        report['estado'] = 'ERROR'
        report['error'] = str(exc)
        logger.exception('ORQUESTACIÓN DETENIDA; sin reintento de escrituras')
    finally:
        report['fin_utc'] = datetime.now(timezone.utc).isoformat()
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        logger.info('Resumen guardado: %s', report_path)
    return 0 if report['estado'] == 'OK' else 1


if __name__ == '__main__':
    sys.exit(main())
