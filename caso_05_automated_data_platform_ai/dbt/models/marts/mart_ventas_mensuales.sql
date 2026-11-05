{{ config(materialized='view') }}

-- Los importes se calculan sobre los flags comerciales ya definidos en PostgreSQL.
-- No se fuerza la inclusión de registros fuera de alcance.
with lineas as (
  select
    date_trunc(fecha_dia, month) as mes,
    id_linea,
    factura,
    cliente_id,
    producto,
    cantidad,
    importe_gbp,
    incluir_ventas_brutas,
    incluir_abonos_mercancia,
    incluir_demanda_unidades
  from {{ ref('stg_movimientos') }}
)
select
  mes,
  count(*) as lineas_totales,
  countif(incluir_ventas_brutas = 1) as lineas_venta,
  count(distinct if(incluir_ventas_brutas = 1, factura, null)) as facturas_venta,
  count(distinct if(incluir_ventas_brutas = 1, cliente_id, null)) as clientes_venta,
  sum(if(incluir_ventas_brutas = 1, importe_gbp, 0)) as ventas_brutas_gbp,
  sum(if(incluir_abonos_mercancia = 1, importe_gbp, 0)) as abonos_mercancia_gbp,
  sum(if(incluir_ventas_brutas = 1 or incluir_abonos_mercancia = 1, importe_gbp, 0)) as ventas_netas_gbp,
  sum(if(incluir_demanda_unidades = 1, cantidad, 0)) as unidades_demanda
from lineas
group by 1
