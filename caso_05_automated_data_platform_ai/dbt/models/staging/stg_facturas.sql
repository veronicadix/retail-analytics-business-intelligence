{{ config(materialized='view') }}

select
  cast(factura as string) as factura,
  cast(cliente_id as string) as cliente_id,
  cast(pais as string) as pais,
  cast(fecha_factura as datetime) as fecha_factura,
  cast(ultima_fecha_linea as datetime) as ultima_fecha_linea,
  cast(flag_varias_horas as int64) as flag_varias_horas,
  cast(lineas_mercancia as int64) as lineas_mercancia,
  cast(unidades_mercancia as numeric) as unidades_mercancia,
  cast(importe_bruto_mercancia_gbp as numeric) as importe_bruto_mercancia_gbp,
  cast(incluir_recompra as int64) as incluir_recompra
from {{ source('retail_raw', 'facturas_venta') }}
