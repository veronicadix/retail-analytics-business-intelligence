"""V16: informe comercial reproducible desde vistas agregadas BigQuery.

Uso: python informe_comercial.py --local
     python informe_comercial.py --claude  (opcional; API con costo)
No actualiza tablas, no envía información personal, no procesa raw localmente.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
from decimal import Decimal
from collections import defaultdict

PROJECT = "retail-data-engineering-512100"
DATASET = "retail_analytics"
MAX_PRODUCTS = 10
MAX_INPUT_CHARS = 12000


def normalize(value):
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def query_one(client, sql):
    rows = list(client.query(sql, location="us-central1").result(max_results=1))
    if not rows:
        raise ValueError("Consulta resumen sin resultados")
    return {k: normalize(v) for k, v in dict(rows[0].items()).items()}


def load_metrics():
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT, location="us-central1")
    summary_sql = f"SELECT * FROM `{PROJECT}.{DATASET}.vw_resumen_comercial`"
    products_sql = f"""SELECT producto,
       ROUND(SUM(ventas_netas_mercancia_gbp),2) AS ventas_netas_gbp,
       ROUND(SUM(ventas_brutas_gbp),2) AS ventas_brutas_gbp,
       ROUND(SUM(abonos_mercancia_gbp),2) AS abonos_gbp,
       SUM(unidades_venta_observadas) AS unidades
    FROM `{PROJECT}.{DATASET}.vw_producto_mes`
    GROUP BY producto ORDER BY ventas_netas_gbp DESC LIMIT {MAX_PRODUCTS}"""
    summary = query_one(client, summary_sql)
    products = [{k: normalize(v) for k, v in dict(row.items()).items()}
                for row in client.query(products_sql, location="us-central1").result(max_results=MAX_PRODUCTS)]
    if not products:
        raise ValueError("La vista de productos no devolvió datos")
    return {"fuente": f"{PROJECT}.{DATASET}", "resumen": summary,
            "top_productos": products, "fecha_extraccion_utc": dt.datetime.now(dt.timezone.utc).isoformat()}



def enrich_products_from_postgres(data):
    """Read-only: agrega filas de la vista por CÓDIGO antes de calcular Pareto/ABC.

    Una referencia puede tener varias descripciones (y por tanto varias filas en
    vw_pareto_productos). No debe clasificarse dos veces un mismo código.
    Los importes se agrupan antes de recalcular los umbrales A/B/C.
    """
    import psycopg
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")

    params = {"host": os.getenv("PGHOST", "localhost"),
              "port": os.getenv("PGPORT", "5432"),
              "dbname": os.getenv("PGDATABASE", "portafolio_retail"),
              "user": os.getenv("PGUSER", "postgres"),
              "password": os.getenv("PGPASSWORD", "")}
    if not params["password"]:
        raise RuntimeError("No se encontró PGPASSWORD en el .env de V16")

    sql = """SELECT producto, descripcion_referencia, ventas_netas_gbp
             FROM public.vw_pareto_productos"""
    with psycopg.connect(**params, connect_timeout=10,
                         options="-c default_transaction_read_only=on") as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            records = cur.fetchall()
    if not records:
        raise RuntimeError("vw_pareto_productos no devolvió registros")

    # Una fila final por código, aun cuando existan varias descripciones.
    grouped = {}
    for code, description, amount in records:
        key = str(code).strip().upper()
        if not key:
            continue
        amount = Decimal(str(amount or 0))
        rec = grouped.setdefault(key, {"net": Decimal("0"), "descriptions": {}})
        rec["net"] += amount
        desc = str(description or "").strip()
        if desc:
            rec["descriptions"][desc] = rec["descriptions"].get(desc, Decimal("0")) + amount

    # Pareto correcto: el orden y acumulado se calculan sobre códigos únicos.
    ranking = sorted(((code, item) for code, item in grouped.items() if item["net"] > 0),
                     key=lambda pair: (-pair[1]["net"], pair[0]))
    total = sum((item["net"] for _, item in ranking), Decimal("0"))
    if total <= 0:
        raise RuntimeError("No hay ventas netas positivas para calcular ABC")

    mapping = {}
    abc = defaultdict(lambda: {"productos": 0, "ventas_netas_gbp": 0.0})
    accumulated = Decimal("0")
    for code, item in ranking:
        amount = item["net"]
        previous_pct = Decimal("100") * accumulated / total
        category = "A" if previous_pct < 80 else ("B" if previous_pct < 95 else "C")
        accumulated += amount
        descriptions = item["descriptions"]
        description = (sorted(descriptions.items(), key=lambda pair: (-pair[1], pair[0]))[0][0]
                       if descriptions else "Sin descripción")
        mapping[code] = {
            "descripcion": description,
            "categoria_abc": category,
            "participacion_pct": float(Decimal("100") * amount / total),
            "acumulado_pct": float(Decimal("100") * accumulated / total),
        }
        abc[category]["productos"] += 1
        abc[category]["ventas_netas_gbp"] += float(amount)

    missing = []
    for product in data["top_productos"]:
        key = str(product["producto"]).strip().upper()
        if key in mapping:
            product.update(mapping[key])
        else:
            missing.append(key)
            product.update({"descripcion": "No encontrado en vista ABC",
                            "categoria_abc": "N/D", "participacion_pct": None,
                            "acumulado_pct": None})
    data["abc"] = {cat: {**abc[cat],
                         "participacion_ventas_positivas_pct":
                         100 * abc[cat]["ventas_netas_gbp"] / float(total)}
                   for cat in ("A", "B", "C")}
    data["abc_total_positivo_gbp"] = float(total)
    data["productos_sin_coincidencia"] = missing
    data["fuente_catalogo_abc"] = "PostgreSQL public.vw_pareto_productos (agregada por código; ABC recalculado)"
    data["codigos_con_multiples_filas"] = len(records) - len(grouped)
    return data


def pct_refunds(net, gross, refund):
    # Abonos frente a ventas BRUTAS, nunca frente a ventas netas.
    gross = float(gross or 0)
    return f"{100 * abs(float(refund or 0)) / gross:.2f}%" if gross > 0 else "N/D"


def safe_markdown(v):
    return str(v).replace("|", "/").replace("\n", " ").replace("\r", " ")

def number(x):
    return f"{float(x):,.2f}" if x is not None else "N/D"


def report_local(data):
    m = data["resumen"]
    lines = ["# Informe comercial enriquecido — V16", "",
             f"Generado UTC: {data['fecha_extraccion_utc']}",
             f"Indicadores: `{data['fuente']}` (BigQuery)",
             f"Nombres y ABC: `{data['fuente_catalogo_abc']}`", "",
             "## Resumen ejecutivo", "",
             f"- Ventas brutas: GBP {number(m.get('ventas_brutas_gbp'))}",
             f"- Abonos de mercancía: GBP {number(m.get('abonos_mercancia_gbp'))}",
             f"- Ventas netas: GBP {number(m.get('ventas_netas_gbp'))}",
             f"- Tasa de abonos sobre ventas brutas: {pct_refunds(m.get('ventas_netas_gbp'), m.get('ventas_brutas_gbp'), m.get('abonos_mercancia_gbp'))}",
             f"- Unidades observadas: {m.get('unidades_vendidas')}",
             f"- Facturas: {m.get('facturas_venta')}",
             f"- Cobertura temporal: {m.get('fecha_minima')} — {m.get('fecha_maxima')}", "",
             "## Top 10: productos con nombres y clasificación ABC", "",
             "| Código | Descripción | Ventas netas GBP | Abonos GBP | % abonos / bruto | ABC |",
             "|---|---|---:|---:|---:|:---:|"]
    for p in data["top_productos"]:
        lines.append("| " + " | ".join([
            safe_markdown(p.get("producto", "")),
            safe_markdown(p.get("descripcion", "N/D")),
            number(p.get("ventas_netas_gbp")), number(p.get("abonos_gbp")),
            pct_refunds(p.get("ventas_netas_gbp"), p.get("ventas_brutas_gbp"), p.get("abonos_gbp")),
            safe_markdown(p.get("categoria_abc", "N/D"))]) + " |")
    lines += ["", "## Pareto ABC del catálogo completo (PostgreSQL)", "",
              "| Categoría | Productos | Ventas netas positivas GBP | Participación sobre ventas positivas |",
              "|:---:|---:|---:|---:|"]
    for category in ("A", "B", "C"):
        a = data["abc"][category]
        lines.append(f"| {category} | {a['productos']:,} | {number(a['ventas_netas_gbp'])} | {a['participacion_ventas_positivas_pct']:.2f}% |")
    lines += ["", f"**Base Pareto:** GBP {number(data['abc_total_positivo_gbp'])} (solo productos de neto positivo).",
              "El porcentaje ABC no usa como denominador las ventas netas globales; la vista excluye filas con ventas netas no positivas.", "",
              f"**Control de granularidad:** {data['codigos_con_multiples_filas']} filas adicionales por códigos repetidos se consolidaron antes del ABC.", ""]
    if data["productos_sin_coincidencia"]:
        lines.append("**Atención:** códigos del top 10 sin coincidencia en PostgreSQL: " +
                     ", ".join(map(safe_markdown, data["productos_sin_coincidencia"])) + ".")
        lines.append("")
    lines += ["## Observaciones y acciones por verificar", "",
              "- Priorizar la revisión comercial de productos A, sin asumir automáticamente que requieren más inventario.",
              "- Investigar motivos de abonos/devoluciones; su importe no demuestra por sí solo un defecto.",
              "- Verificar existencias, márgenes y estacionalidad antes de recomendar compras.",
              "- No interpretar diciembre de 2011 como mes completo ni inferir tendencias actuales de datos 2009–2011.",
              "- La descripción y el ABC proceden de PostgreSQL; el ranking financiero del Top 10 procede de BigQuery.",
              "- Este informe presenta observaciones, no pronósticos ni causalidad comprobada."]
    return "\n".join(lines) + "\n"


def claude_analysis(data):
    """Opcional: una llamada; Anthropic factura API independientemente de Claude Pro."""
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Falta ANTHROPIC_API_KEY; usa --local (gratis)")
    from anthropic import Anthropic
    payload = json.dumps(data, ensure_ascii=False, default=str)
    if len(payload) > MAX_INPUT_CHARS:
        raise ValueError("Datos agregados superan el limite local configurado")
    prompt = ("Analiza exclusivamente estas métricas comerciales agregadas. "
              "Responde en español, con 3 hallazgos, 3 acciones, evidencia numérica "
              "para cada hallazgo, 2 limitaciones y sin inventar causalidad. "
              "No son datos actuales: corresponden a 2009-2011. "
              "El último mes puede estar incompleto. Si un dato no permite inferir algo, dilo.\n\n" + payload)
    client = Anthropic(api_key=key, timeout=35.0, max_retries=0)
    answer = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        max_tokens=650, temperature=0,
        messages=[{"role": "user", "content": prompt}])
    return "\n".join(block.text for block in answer.content if getattr(block, "type", "") == "text")


def main():
    ap = argparse.ArgumentParser(description="Informe agregado BigQuery + Claude opcional")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--local", action="store_true", help="Solo BigQuery; no invoca Claude (predeterminado)")
    mode.add_argument("--claude", action="store_true", help="Habilita una llamada API de pago")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = root / "salidas"
    out.mkdir(parents=True, exist_ok=True)
    # Salidas generadas permanecen locales: excluidas de GitHub.
    data = enrich_products_from_postgres(load_metrics())
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out / f"informe_comercial_{stamp}.md"
    content = report_local(data)
    if args.claude:
        # No generar ni guardar salida parcial si la llamada pagada falla.
        content += "\n## Análisis asistido por Claude (no verificado)\n\n" + claude_analysis(data) + "\n"
    path.write_text(content, encoding="utf-8")
    print("Informe guardado:", path)
    print("Modo:", "BigQuery + Claude API" if args.claude else "BigQuery local (sin Claude API)")

if __name__ == "__main__":
    main()
