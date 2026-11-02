-- Etapa 2 / Control mínimo de carga
-- Ejecutar en BigQuery Standard SQL; solo lectura.
-- Fuente: CSV exportado de PostgreSQL, 13 columnas sin identificador de cliente.
SELECT
  COUNT(*) AS total_movimientos,
  SUM(IF(incluir_ventas_brutas = 1, importe_gbp, 0)) AS ventas_brutas_gbp,
  SUM(IF(incluir_abonos_mercancia = 1, importe_gbp, 0)) AS abonos_mercancia_gbp,
  SUM(IF(incluir_ventas_brutas = 1 OR incluir_abonos_mercancia = 1, importe_gbp, 0)) AS ventas_netas_gbp
FROM `retail-data-engineering-512100.retail_analytics.movimientos_raw`;
