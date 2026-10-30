-- Datos agregados. Evitar dimensiones personales o identificadores de clientes.
-- Último mes parcial (diciembre 2011) se excluye de comparaciones temporales.
SELECT producto, ROUND(SUM(ventas_netas_mercancia_gbp),2) AS ventas_netas_gbp,
       ROUND(SUM(ventas_brutas_gbp),2) AS ventas_brutas_gbp,
       ROUND(SUM(abonos_mercancia_gbp),2) AS abonos_gbp,
       SUM(unidades_venta_observadas) AS unidades
FROM `retail-data-engineering-512100.retail_analytics.vw_producto_mes`
GROUP BY producto
ORDER BY ventas_netas_gbp DESC LIMIT 10;
