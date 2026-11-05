{{ config(materialized='view') }}

select
  cast(id_linea as string) as id_linea,
  cast(factura as string) as factura,
  cast(producto as string) as producto,
  cast(descripcion as string) as descripcion,
  cast(cliente_id as string) as cliente_id,
  cast(pais as string) as pais,
  cast(fecha as datetime) as fecha,
  date(fecha) as fecha_dia,
  cast(cantidad as numeric) as cantidad,
  cast(precio_gbp as numeric) as precio_gbp,
  cast(importe_gbp as numeric) as importe_gbp,
  cast(clase_codigo as string) as clase_codigo,
  cast(tipo_movimiento as string) as tipo_movimiento,
  cast(incluir_ventas_brutas as int64) as incluir_ventas_brutas,
  cast(incluir_abonos_mercancia as int64) as incluir_abonos_mercancia,
  cast(incluir_recompra as int64) as incluir_recompra,
  cast(incluir_demanda_unidades as int64) as incluir_demanda_unidades,
  cast(motivo_alcance as string) as motivo_alcance
from {{ source('retail_raw', 'base_movimientos') }}
