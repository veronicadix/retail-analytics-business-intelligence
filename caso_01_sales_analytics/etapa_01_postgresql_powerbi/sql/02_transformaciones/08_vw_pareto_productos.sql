-- ETAPA 1 | Vista Pareto/ABC por producto (implementación ejecutada en pgAdmin).
-- Origen: public.vw_indicadores_producto, previamente creada.
-- Se incluyen solo productos con ventas netas POSITIVAS.
-- Umbrales de la categoría: A hasta alcanzar 80 %, B hasta alcanzar 95 %, C el resto.
-- Los productos que cruzan los umbrales se asignan a la categoría iniciada antes de ellos.
-- No modifica tablas originales.
CREATE OR REPLACE VIEW public.vw_pareto_productos AS
WITH ventas_producto AS (
    -- Métrica base: una fila por producto en la vista existente.
    SELECT producto, descripcion_referencia,
           ventas_netas_mercancia_gbp AS ventas_netas_gbp
    FROM public.vw_indicadores_producto
    WHERE ventas_netas_mercancia_gbp > 0
), acumulados AS (
    -- Ventas totales positivas y acumulado por ranking descendente.
    SELECT *,
           SUM(ventas_netas_gbp) OVER () AS total_ventas_gbp,
           SUM(ventas_netas_gbp) OVER (
               ORDER BY ventas_netas_gbp DESC, producto
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS ventas_acumuladas_gbp
    FROM ventas_producto
)
SELECT producto, descripcion_referencia, ventas_netas_gbp,
       -- Porcentaje individual (escala 0 a 100, NO formato decimal 0 a 1).
       ROUND(100 * ventas_netas_gbp / NULLIF(total_ventas_gbp, 0), 2) AS participacion_pct,
       -- Porcentaje acumulado por posición de ranking.
       ROUND(100 * ventas_acumuladas_gbp / NULLIF(total_ventas_gbp, 0), 2) AS acumulado_pct,
       -- Clasificación basada en porcentaje anterior a este producto.
       CASE
           WHEN 100 * (ventas_acumuladas_gbp - ventas_netas_gbp) /
                NULLIF(total_ventas_gbp, 0) < 80 THEN 'A'
           WHEN 100 * (ventas_acumuladas_gbp - ventas_netas_gbp) /
                NULLIF(total_ventas_gbp, 0) < 95 THEN 'B'
           ELSE 'C'
       END AS categoria_abc
FROM acumulados;
