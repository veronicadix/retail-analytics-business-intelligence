-- Caso 2 / Olist | 04: consultas de indicadores; solo SELECT
-- A. Pedidos, clientes, ventas de productos, ticket y fechas.
SELECT COUNT(*) AS pedidos_entregados,
       COUNT(DISTINCT customer_unique_id) AS compradores_unicos,
       ROUND(SUM(valor_productos_brl),2) AS valor_productos_brl,
       ROUND(AVG(valor_productos_brl),2) AS valor_promedio_pedido_brl,
       MIN(fecha_compra) AS primera_fecha,MAX(fecha_compra) AS ultima_fecha
FROM olist.vw_pedidos_analiticos;

-- B. Compradores con >= 2 pedidos entregados.
WITH compras_cliente AS (
    SELECT customer_unique_id,COUNT(DISTINCT order_id) AS total_pedidos
    FROM olist.vw_pedidos_analiticos GROUP BY customer_unique_id
)
SELECT COUNT(*) AS compradores_unicos,
       COUNT(*) FILTER (WHERE total_pedidos=1) AS compradores_una_vez,
       COUNT(*) FILTER (WHERE total_pedidos>=2) AS compradores_recurrentes,
       ROUND(100.0*COUNT(*) FILTER (WHERE total_pedidos>=2)
             /NULLIF(COUNT(*),0),2) AS tasa_recompra_pct
FROM compras_cliente;

-- C. Retencion ponderada M1, M3 y M6; solo meses de seguimiento completos.
-- Los datos disponibles terminan en agosto de 2018 (mes incompleto).
WITH parametros AS (SELECT DATE '2018-07-01' AS ultimo_mes_completo),
meses_objetivo AS (SELECT mes FROM (VALUES (1),(3),(6)) AS m(mes)),
cohortes AS (
    SELECT DISTINCT mes_cohorte,clientes_iniciales
    FROM olist.vw_cohortes_retencion
),
cohortes_elegibles AS (
    SELECT c.mes_cohorte,c.clientes_iniciales,m.mes
    FROM cohortes c CROSS JOIN meses_objetivo m CROSS JOIN parametros p
    WHERE c.mes_cohorte+(m.mes*INTERVAL '1 month')<=p.ultimo_mes_completo
)
SELECT e.mes AS mes_retencion,COUNT(*) AS cohortes_analizadas,
       SUM(e.clientes_iniciales) AS clientes_iniciales,
       SUM(COALESCE(r.clientes_activos,0)) AS clientes_retenidos,
       ROUND(100.0*SUM(COALESCE(r.clientes_activos,0))
             /NULLIF(SUM(e.clientes_iniciales),0),2) AS retencion_ponderada_pct
FROM cohortes_elegibles e
LEFT JOIN olist.vw_cohortes_retencion r
 ON e.mes_cohorte=r.mes_cohorte AND e.mes=r.mes_desde_primera_compra
GROUP BY e.mes ORDER BY e.mes;

-- D. RFM promedio.
SELECT COUNT(*) AS clientes_rfm,
       ROUND(AVG(recencia_dias),2) AS recencia_promedio_dias,
       ROUND(AVG(frecuencia_pedidos),2) AS frecuencia_promedio,
       ROUND(AVG(valor_monetario_brl),2) AS valor_monetario_promedio_brl
FROM olist.vw_rfm_clientes;

-- E. Distribucion de segmentos.
SELECT segmento_cliente,COUNT(*) AS clientes,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),2) AS porcentaje_clientes,
       ROUND(SUM(valor_monetario_brl),2) AS valor_historico_brl
FROM olist.vw_segmentos_clientes
GROUP BY segmento_cliente ORDER BY clientes DESC;
