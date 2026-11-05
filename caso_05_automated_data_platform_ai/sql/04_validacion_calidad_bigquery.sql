
-- CASO 05
-- 04_validacion_calidad_bigquery.sql
-- Validación de calidad de las tres tablas

SELECT
  'base_movimientos' AS tabla,
  COUNT(*) AS total_registros,
  COUNTIF(id_linea IS NULL) AS claves_nulas,
  COUNT(*) - COUNT(DISTINCT id_linea) AS claves_duplicadas,
  COUNTIF(fecha IS NULL) AS fechas_nulas,
  COUNTIF(cantidad IS NULL) AS cantidades_nulas,
  COUNTIF(importe_gbp IS NULL) AS importes_nulos
FROM
  `maximal-arcade-512100-h2.retail_pipeline_case05.base_movimientos`

UNION ALL

SELECT
  'catalogo_codigos' AS tabla,
  COUNT(*) AS total_registros,
  COUNTIF(producto IS NULL) AS claves_nulas,
  COUNT(*) - COUNT(DISTINCT producto) AS claves_duplicadas,
  CAST(NULL AS INT64) AS fechas_nulas,
  CAST(NULL AS INT64) AS cantidades_nulas,
  CAST(NULL AS INT64) AS importes_nulos
FROM
  `maximal-arcade-512100-h2.retail_pipeline_case05.catalogo_codigos`

UNION ALL

SELECT
  'facturas_venta' AS tabla,
  COUNT(*) AS total_registros,
  COUNTIF(factura IS NULL) AS claves_nulas,
  COUNT(*) - COUNT(DISTINCT factura) AS claves_duplicadas,
  COUNTIF(fecha_factura IS NULL) AS fechas_nulas,
  CAST(NULL AS INT64) AS cantidades_nulas,
  CAST(NULL AS INT64) AS importes_nulos
FROM
  `maximal-arcade-512100-h2.retail_pipeline_case05.facturas_venta`;