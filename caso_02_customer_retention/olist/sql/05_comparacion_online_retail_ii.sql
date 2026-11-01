-- Caso 2 / comparacion separada: no mezclar ni unir los datasets.
-- Olist: clientes unicos con >=2 pedidos entregados.
WITH compras_cliente AS (
 SELECT customer_unique_id, COUNT(DISTINCT order_id) AS pedidos
 FROM olist.vw_pedidos_analiticos GROUP BY customer_unique_id
)
SELECT 'Olist' AS dataset,COUNT(*) AS clientes,
 COUNT(*) FILTER (WHERE pedidos>=2) AS recurrentes,
 ROUND(100.0*COUNT(*) FILTER (WHERE pedidos>=2)/NULLIF(COUNT(*),0),2) AS recompra_pct
FROM compras_cliente;

-- Online Retail II: segun la regla de negocio existente incluir_recompra=1.
WITH compras_cliente AS (
 SELECT cliente_id,COUNT(DISTINCT factura) AS pedidos
 FROM public.base_movimientos
 WHERE cliente_id IS NOT NULL AND incluir_recompra=1
 GROUP BY cliente_id
)
SELECT 'Online Retail II' AS dataset,COUNT(*) AS clientes,
 COUNT(*) FILTER (WHERE pedidos>=2) AS recurrentes,
 ROUND(100.0*COUNT(*) FILTER (WHERE pedidos>=2)/NULLIF(COUNT(*),0),2) AS recompra_pct
FROM compras_cliente;
