{{ config(materialized='view') }}

select
  cast(producto as string) as producto,
  cast(clase_codigo as string) as clase_codigo,
  cast(descripcion_referencia as string) as descripcion_referencia,
  cast(variantes_descripcion_en_ventas as int64) as variantes_descripcion_en_ventas,
  cast(filas_conservadas as int64) as filas_conservadas,
  cast(lineas_venta as int64) as lineas_venta,
  cast(regla_origen as string) as regla_origen
from {{ source('retail_raw', 'catalogo_codigos') }}
