-- Dias (incluyendo fracciones) entre facturas elegibles consecutivas por cliente.
CREATE OR REPLACE VIEW public.vw_intervalos_recompra AS
WITH compras AS (
    SELECT DISTINCT cliente_id, factura, fecha_factura
    FROM public.facturas_venta
    WHERE incluir_recompra = 1
      AND cliente_id IS NOT NULL AND TRIM(cliente_id) <> ''
      AND fecha_factura IS NOT NULL
),
compras_ordenadas AS (
    SELECT cliente_id, factura, fecha_factura,
           LAG(fecha_factura) OVER (
             PARTITION BY cliente_id ORDER BY fecha_factura, factura
           ) AS fecha_compra_anterior
    FROM compras
)
SELECT cliente_id, factura, fecha_factura, fecha_compra_anterior,
       ROUND((EXTRACT(EPOCH FROM (fecha_factura - fecha_compra_anterior))
              / 86400)::numeric, 2) AS dias_entre_compras
FROM compras_ordenadas
WHERE fecha_compra_anterior IS NOT NULL;
