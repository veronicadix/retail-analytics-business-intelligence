-- Etapa 2 / Vista de producto y mes
-- Reproduce las banderas de alcance usadas en la vista equivalente PostgreSQL.
-- DATE(fecha) convierte DATETIME a DATE sin desplazamiento de zona horaria.
CREATE OR REPLACE VIEW `retail-data-engineering-512100.retail_analytics.vw_producto_mes` AS
SELECT
  DATE_TRUNC(DATE(fecha), MONTH) AS mes,
  producto,
  SUM(IF(incluir_demanda_unidades = 1, cantidad, 0)) AS unidades_venta_observadas,
  COUNT(DISTINCT IF(incluir_ventas_brutas = 1, factura, NULL)) AS facturas_venta,
  SUM(IF(incluir_ventas_brutas = 1, importe_gbp, 0)) AS ventas_brutas_gbp,
  SUM(IF(incluir_abonos_mercancia = 1, importe_gbp, 0)) AS abonos_mercancia_gbp,
  SUM(IF(incluir_ventas_brutas = 1 OR incluir_abonos_mercancia = 1, importe_gbp, 0)) AS ventas_netas_mercancia_gbp
FROM `retail-data-engineering-512100.retail_analytics.movimientos_raw`
WHERE incluir_ventas_brutas = 1
   OR incluir_abonos_mercancia = 1
   OR incluir_demanda_unidades = 1
GROUP BY mes, producto;
