-- CASO 05 - Conciliacion de importes y unidades
-- Compara calculos de la fuente BigQuery con el mart mensual dbt.
-- No modifica tablas. Ubicacion de ejecucion: US.
WITH fuente AS (
  SELECT
    COUNT(*) AS lineas_totales,
    COUNTIF(incluir_ventas_brutas = 1) AS lineas_venta,
    SUM(IF(incluir_ventas_brutas = 1, importe_gbp, 0)) AS ventas_brutas_gbp,
    SUM(IF(incluir_abonos_mercancia = 1, importe_gbp, 0)) AS abonos_mercancia_gbp,
    SUM(IF(incluir_ventas_brutas = 1 OR incluir_abonos_mercancia = 1, importe_gbp, 0)) AS ventas_netas_gbp,
    SUM(IF(incluir_demanda_unidades = 1, cantidad, 0)) AS unidades_demanda
  FROM `maximal-arcade-512100-h2.retail_pipeline_case05.base_movimientos`
),
mart AS (
  SELECT
    SUM(lineas_totales) AS lineas_totales,
    SUM(lineas_venta) AS lineas_venta,
    SUM(ventas_brutas_gbp) AS ventas_brutas_gbp,
    SUM(abonos_mercancia_gbp) AS abonos_mercancia_gbp,
    SUM(ventas_netas_gbp) AS ventas_netas_gbp,
    SUM(unidades_demanda) AS unidades_demanda
  FROM `maximal-arcade-512100-h2.retail_case05_dbt.mart_ventas_mensuales`
),
comparacion AS (
  SELECT 'lineas_totales' AS metrica, CAST(f.lineas_totales AS NUMERIC) AS valor_fuente, CAST(m.lineas_totales AS NUMERIC) AS valor_mart FROM fuente f CROSS JOIN mart m
  UNION ALL SELECT 'lineas_venta', CAST(f.lineas_venta AS NUMERIC), CAST(m.lineas_venta AS NUMERIC) FROM fuente f CROSS JOIN mart m
  UNION ALL SELECT 'ventas_brutas_gbp', f.ventas_brutas_gbp, m.ventas_brutas_gbp FROM fuente f CROSS JOIN mart m
  UNION ALL SELECT 'abonos_mercancia_gbp', f.abonos_mercancia_gbp, m.abonos_mercancia_gbp FROM fuente f CROSS JOIN mart m
  UNION ALL SELECT 'ventas_netas_gbp', f.ventas_netas_gbp, m.ventas_netas_gbp FROM fuente f CROSS JOIN mart m
  UNION ALL SELECT 'unidades_demanda', f.unidades_demanda, m.unidades_demanda FROM fuente f CROSS JOIN mart m
)
SELECT metrica, valor_fuente, valor_mart,
       valor_mart - valor_fuente AS diferencia,
       IF(valor_mart = valor_fuente, 'OK', 'REVISAR') AS estado
FROM comparacion
ORDER BY metrica;
