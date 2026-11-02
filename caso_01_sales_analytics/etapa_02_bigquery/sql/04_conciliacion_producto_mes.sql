-- Etapa 2 / Conciliación puntual entre agregados de BigQuery.
-- Solo lectura. Esperado: 67.205 combinaciones producto-mes y métricas del resumen.
SELECT COUNT(*) AS registros_producto_mes,
       SUM(unidades_venta_observadas) AS unidades_vendidas,
       SUM(ventas_brutas_gbp) AS ventas_brutas_gbp,
       SUM(abonos_mercancia_gbp) AS abonos_gbp,
       SUM(ventas_netas_mercancia_gbp) AS ventas_netas_gbp
FROM `retail-data-engineering-512100.retail_analytics.vw_producto_mes`;
