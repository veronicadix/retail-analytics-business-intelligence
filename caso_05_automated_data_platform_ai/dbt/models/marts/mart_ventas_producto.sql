{{ config(materialized='view') }}

with movimientos as (
  select
    producto,
    factura,
    cliente_id,
    cantidad,
    importe_gbp,
    incluir_ventas_brutas,
    incluir_abonos_mercancia,
    incluir_demanda_unidades
  from {{ ref('stg_movimientos') }}
), catalogo as (
  select producto, descripcion_referencia, clase_codigo
  from {{ ref('stg_productos') }}
), agregado as (
  select
    producto,
    countif(incluir_ventas_brutas = 1) as lineas_venta,
    count(distinct if(incluir_ventas_brutas = 1, factura, null)) as facturas_venta,
    count(distinct if(incluir_ventas_brutas = 1, cliente_id, null)) as clientes_venta,
    sum(if(incluir_ventas_brutas = 1, importe_gbp, 0)) as ventas_brutas_gbp,
    sum(if(incluir_abonos_mercancia = 1, importe_gbp, 0)) as abonos_mercancia_gbp,
    sum(if(incluir_ventas_brutas = 1 or incluir_abonos_mercancia = 1, importe_gbp, 0)) as ventas_netas_gbp,
    sum(if(incluir_demanda_unidades = 1, cantidad, 0)) as unidades_demanda
  from movimientos
  group by producto
)
select
  a.*,
  c.descripcion_referencia,
  c.clase_codigo
from agregado a
left join catalogo c using (producto)
