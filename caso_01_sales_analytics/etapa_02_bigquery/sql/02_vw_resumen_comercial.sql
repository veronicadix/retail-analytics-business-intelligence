-- Etapa 2 / Vista de indicadores comerciales
-- Ejecutar en BigQuery Standard SQL; CREATE OR REPLACE VIEW no altera movimientos_raw.
CREATE OR REPLACE VIEW `retail-data-engineering-512100.retail_analytics.vw_resumen_comercial` AS
SELECT
  COUNT(*) AS total_movimientos,
  SUM(IF(incluir_ventas_brutas = 1, importe_gbp, 0)) AS ventas_brutas_gbp,
  SUM(IF(incluir_abonos_mercancia = 1, importe_gbp, 0)) AS abonos_mercancia_gbp,
  SUM(IF(incluir_ventas_brutas = 1 OR incluir_abonos_mercancia = 1, importe_gbp, 0)) AS ventas_netas_gbp,
  SUM(IF(incluir_demanda_unidades = 1, cantidad, 0)) AS unidades_vendidas,
  COUNT(DISTINCT IF(incluir_ventas_brutas = 1, factura, NULL)) AS facturas_venta,
  MIN(fecha) AS fecha_minima,
  MAX(fecha) AS fecha_maxima
FROM `retail-data-engineering-512100.retail_analytics.movimientos_raw`;
