-- Caso 2 / Olist | 03: RFM y grupos comerciales exploratorios
-- Fecha de referencia: un dia posterior a la ultima compra del dataset.
CREATE OR REPLACE VIEW olist.vw_rfm_clientes AS
WITH fecha_referencia AS (
    SELECT MAX(fecha_compra)+1 AS fecha_corte
    FROM olist.vw_pedidos_analiticos
)
SELECT p.customer_unique_id, MAX(p.fecha_compra) AS ultima_compra,
       MAX(f.fecha_corte)-MAX(p.fecha_compra) AS recencia_dias,
       COUNT(DISTINCT p.order_id) AS frecuencia_pedidos,
       ROUND(SUM(p.valor_productos_brl),2) AS valor_monetario_brl
FROM olist.vw_pedidos_analiticos p
CROSS JOIN fecha_referencia f
GROUP BY p.customer_unique_id;

CREATE OR REPLACE VIEW olist.vw_segmentos_clientes AS
SELECT customer_unique_id,ultima_compra,recencia_dias,frecuencia_pedidos,
       valor_monetario_brl,
       CASE
         WHEN frecuencia_pedidos>=2 AND recencia_dias<=90 THEN 'Recurrentes recientes'
         WHEN frecuencia_pedidos>=2 AND recencia_dias>90 THEN 'Recurrentes antiguos'
         WHEN frecuencia_pedidos=1 AND recencia_dias<=90 THEN 'Primera compra reciente'
         ELSE 'Compra unica antigua'
       END AS segmento_cliente
FROM olist.vw_rfm_clientes;
