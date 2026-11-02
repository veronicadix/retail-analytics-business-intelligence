-- Ejecutar en pgAdmin / base de datos portafolio_retail.
-- En Query Tool, ejecutar y luego usar Data Output > Save results to file (CSV).
-- Nombre sugerido: 06_detalle_cohortes_olist.csv
SELECT
    mes_cohorte,
    mes_desde_primera_compra,
    clientes_iniciales,
    clientes_activos,
    retencion_pct
FROM olist.vw_cohortes_retencion
ORDER BY mes_cohorte, mes_desde_primera_compra;
