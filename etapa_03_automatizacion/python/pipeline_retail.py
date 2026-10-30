"""
ETAPA 3 - Pipeline PostgreSQL -> BigQuery.
Uso:
  python etapa_03_automatizacion/python/pipeline_retail.py --check
  python etapa_03_automatizacion/python/pipeline_retail.py --run

--check valida conexiones y calcula conteos, sin escribir.
--run exporta CSV sin datos personales, carga en staging y reemplazo controlado de raw mediante COPY job.
No almacenar credenciales ni subir datos/logs al repositorio.
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
import csv
import logging
import os
import tempfile
import time
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPICallError, ServiceUnavailable, TooManyRequests
from google.cloud import bigquery

PROJECT = "retail-data-engineering-512100"
DATASET = "retail_analytics"
RAW = f"{PROJECT}.{DATASET}.movimientos_raw"
STAGE = f"{PROJECT}.{DATASET}.movimientos_stage"
FIELDS = [
    "id_linea", "factura", "producto", "cantidad", "fecha", "precio_gbp",
    "importe_gbp", "clase_codigo", "tipo_movimiento",
    "incluir_ventas_brutas", "incluir_abonos_mercancia",
    "incluir_recompra", "incluir_demanda_unidades",
]
SCHEMA = [
    bigquery.SchemaField(name, dtype)
    for name, dtype in [
        ("id_linea", "STRING"), ("factura", "STRING"), ("producto", "STRING"),
        ("cantidad", "NUMERIC"), ("fecha", "DATETIME"),
        ("precio_gbp", "NUMERIC"), ("importe_gbp", "NUMERIC"),
        ("clase_codigo", "STRING"), ("tipo_movimiento", "STRING"),
        ("incluir_ventas_brutas", "INTEGER"),
        ("incluir_abonos_mercancia", "INTEGER"),
        ("incluir_recompra", "INTEGER"),
        ("incluir_demanda_unidades", "INTEGER"),
    ]
]
EXPORT_QUERY = """
COPY (
    SELECT id_linea, factura, producto, cantidad, fecha, precio_gbp,
           importe_gbp, clase_codigo, tipo_movimiento,
           incluir_ventas_brutas, incluir_abonos_mercancia,
           incluir_recompra, incluir_demanda_unidades
    FROM public.base_movimientos
    ORDER BY id_linea
) TO STDOUT WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8')
"""


def retry_call(fn, label, attempts=3):
    """Reintentar solo fallos temporales de Google Cloud, con espera incremental."""
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except (ServiceUnavailable, TooManyRequests) as exc:
            if attempt == attempts:
                raise
            pause = 2 ** attempt
            logging.warning("%s: intento %d falló (%s); esperando %ds", label, attempt, exc, pause)
            time.sleep(pause)


def pg_connect():
    """Abrir PostgreSQL usando variables de entorno, sin contraseñas en código."""
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "portafolio_retail"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.environ["PGPASSWORD"],
        connect_timeout=15,
    )


def export_copy(conn, output):
    """COPY transmite filas completas del servidor a un archivo CSV local."""
    with conn.cursor() as cur, open(output, "wb") as file:
        with cur.copy(EXPORT_QUERY) as copy:
            for chunk in copy:
                file.write(chunk)


def pipeline_main():
    parser = argparse.ArgumentParser(description="Pipeline comercial seguro")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Solo comprobaciones, sin escrituras")
    group.add_argument("--run", action="store_true", help="Carga staging y reemplazo raw; requiere autorización")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not os.getenv("PGPASSWORD"):
        raise SystemExit("Falta PGPASSWORD. Configura .env local según .env.example.")
    client = bigquery.Client(project=PROJECT, location="us-central1")
    with pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM public.base_movimientos")
            source_count = cur.fetchone()[0]
        dest_count = retry_call(lambda: client.get_table(RAW).num_rows, "metadatos BigQuery")
        logging.info("PostgreSQL=%s; BigQuery raw=%s", source_count, dest_count)
        if args.check:
            logging.info("CHECK correcto. No se escribieron datos.")
            return

        # En modo --run: exportar solo columnas aprobadas, en archivo temporal.
        with tempfile.TemporaryDirectory(prefix="retail_pipeline_") as tmp:
            csv_file = Path(tmp) / "movimientos.csv"
            export_copy(conn, csv_file)
            logging.info("CSV temporal generado: %s bytes", csv_file.stat().st_size)

            # Staging se reemplaza por completo; reejecutar no acumula copias.
            config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                schema=SCHEMA,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                max_bad_records=0,
            )
            with csv_file.open("rb") as file:
                job = retry_call(lambda: client.load_table_from_file(
                    file, STAGE, job_config=config, location="us-central1"
                ), "carga staging")
            job.result()
            logging.info("Staging cargado; job_id=%s", job.job_id)

        # Verificar unicidad antes de MERGE: una misma clave no puede actualizar varias veces.
        stats = list(client.query(
            f"SELECT COUNT(*) n, COUNT(DISTINCT id_linea) u, "
            f"COUNTIF(id_linea IS NULL) missing FROM `{STAGE}`",
            location="us-central1",
        ).result())[0]
        if stats.n != source_count or stats.n != stats.u or stats.missing:
            raise RuntimeError(
                f"Staging no conciliado: filas={stats.n}, unicas={stats.u}, "
                f"nulas={stats.missing}, esperado={source_count}"
            )

        # La tabla raw existente conserva claves. Detectar duplicados preexistentes
        # antes de una actualización para no esconder problemas de origen.
        existing = list(client.query(
            f"SELECT COUNT(*) n, COUNT(DISTINCT id_linea) u "
            f"FROM `{RAW}`", location="us-central1"
        ).result())[0]
        if existing.n != existing.u:
            raise RuntimeError("Tabla raw tiene id_linea duplicado; revisar antes del MERGE.")

        # Sandbox no permite MERGE (DML). Un copy job sobrescribe raw de manera
        # atómica con las filas previamente verificadas en staging.
        # Esta estrategia NO es incremental: es una sustitución completa.
        copy_config = bigquery.CopyJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            create_disposition=bigquery.CreateDisposition.CREATE_NEVER,
        )
        copy_job = client.copy_table(
            sources=STAGE,
            destination=RAW,
            job_config=copy_config,
            location="us-central1",
        )
        copy_job.result()
        logging.info("Copia validada a raw completada; job_id=%s", copy_job.job_id)
        # La tabla raw conserva un único conjunto completo; volver a ejecutar
        # reemplaza la carga, en lugar de anexar duplicados.
        final_rows = client.get_table(RAW).num_rows
        if final_rows != source_count:
            raise RuntimeError(
                f"Raw no coincide tras COPY: filas={final_rows}; esperado={source_count}"
            )
        logging.info("Pipeline finalizado correctamente; raw=%s registros", final_rows)



def utc_now():
    """Fecha UTC en formato ISO 8601 para comparar ejecuciones."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_history(history_path, record):
    """Guardar resumen JSONL local sin credenciales ni datos individuales."""
    with history_path.open("a", encoding="utf-8") as log:
        log.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    """Control operacional: bloqueo exclusivo, logs persistentes y duración."""
    root = Path(__file__).resolve().parents[2]
    logs = root / "etapa_03_automatizacion" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:12]
    started = utc_now()
    start_clock = time.monotonic()
    lock_path = logs / "pipeline.lock"
    history_path = logs / "historial_ejecuciones.jsonl"
    details_path = logs / "pipeline.log"
    mode = "--run" if "--run" in sys.argv else "--check"

    # O_EXCL falla si ya existe un bloqueo; nunca se ejecutan dos cargas en paralelo.
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(
            "Ya existe un bloqueo de ejecución (etapa_03_automatizacion/logs/pipeline.lock). "
            "Comprueba que no haya otro pipeline activo. Si quedó por un cierre "
            "inesperado, elimínalo manualmente solo después de comprobarlo."
        )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(f"id={run_id}\nstarted_utc={started}\n")

    # El archivo se registra solo después de conseguir el bloqueo.
    handler = logging.FileHandler(details_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    # Registrar INFO tanto en archivo como en la consola.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(console_handler)
    outcome = "ERROR"
    err_type = None
    try:
        logging.info("Ejecución id=%s modo=%s iniciada", run_id, mode)
        pipeline_main()
        outcome = "OK"
    except Exception as exc:
        # No almacenar valores de excepción: podrían incluir rutas o información sensible.
        err_type = type(exc).__name__
        logging.error("Ejecución id=%s falló; tipo=%s", run_id, err_type)
        raise
    finally:
        elapsed = round(time.monotonic() - start_clock, 2)
        write_history(history_path, {
            "id": run_id, "modo": mode, "inicio_utc": started,
            "fin_utc": utc_now(), "duracion_segundos": elapsed,
            "estado": outcome, "tipo_error": err_type,
        })
        logging.info("Ejecución id=%s estado=%s duración=%.2fs", run_id, outcome, elapsed)
        logger.removeHandler(handler)
        handler.close()
        logger.removeHandler(console_handler)
        console_handler.close()
        # No borrar bloqueo de otra ejecución accidentalmente.
        try:
            if lock_path.read_text(encoding="utf-8").startswith(f"id={run_id}\n"):
                lock_path.unlink()
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()
