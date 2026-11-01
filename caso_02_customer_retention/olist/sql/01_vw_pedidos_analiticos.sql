-- Caso 2 / Olist | 01: una fila por pedido entregado
-- Moneda BRL. Separa valor de productos y flete.
CREATE OR REPLACE VIEW olist.vw_pedidos_analiticos AS
WITH valor_pedidos AS (
    SELECT order_id,
           COUNT(*) AS numero_articulos,
           SUM(price) AS valor_productos_brl,
           SUM(freight_value) AS valor_flete_brl
    FROM olist.order_items
    GROUP BY order_id
)
SELECT o.order_id,
       c.customer_unique_id,
       c.customer_state,
       o.order_status,
       o.order_purchase_timestamp::date AS fecha_compra,
       DATE_TRUNC('month', o.order_purchase_timestamp)::date AS mes_compra,
       COALESCE(v.numero_articulos, 0) AS numero_articulos,
       COALESCE(v.valor_productos_brl, 0) AS valor_productos_brl,
       COALESCE(v.valor_flete_brl, 0) AS valor_flete_brl
FROM olist.orders o
JOIN olist.customers c ON o.customer_id = c.customer_id
LEFT JOIN valor_pedidos v ON o.order_id = v.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp IS NOT NULL
  AND c.customer_unique_id IS NOT NULL;
