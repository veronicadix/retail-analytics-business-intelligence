-- Cohortes por mes de primera compra elegible; retencion mensual NO consecutiva.
CREATE OR REPLACE VIEW public.vw_cohortes_retencion AS
WITH compras_validas AS (
    SELECT DISTINCT cliente_id, factura,
           DATE_TRUNC('month', fecha_factura)::date AS mes_compra
    FROM public.facturas_venta
    WHERE incluir_recompra = 1
      AND cliente_id IS NOT NULL AND TRIM(cliente_id) <> ''
      AND fecha_factura IS NOT NULL
),
primera_compra AS (
    SELECT cliente_id, MIN(mes_compra) AS mes_cohorte
    FROM compras_validas GROUP BY cliente_id
),
actividad_mensual AS (
    SELECT DISTINCT c.cliente_id, p.mes_cohorte, c.mes_compra,
           ((EXTRACT(YEAR FROM c.mes_compra) - EXTRACT(YEAR FROM p.mes_cohorte)) * 12
             + EXTRACT(MONTH FROM c.mes_compra) - EXTRACT(MONTH FROM p.mes_cohorte))::integer
             AS mes_desde_primera_compra
    FROM compras_validas c
    JOIN primera_compra p ON c.cliente_id = p.cliente_id
),
tamano_cohortes AS (
    SELECT mes_cohorte, COUNT(*) AS clientes_iniciales
    FROM primera_compra GROUP BY mes_cohorte
)
SELECT a.mes_cohorte, a.mes_desde_primera_compra,
       t.clientes_iniciales,
       COUNT(DISTINCT a.cliente_id) AS clientes_activos,
       ROUND(COUNT(DISTINCT a.cliente_id)::numeric
         / NULLIF(t.clientes_iniciales, 0) * 100, 2) AS retencion_pct
FROM actividad_mensual a
JOIN tamano_cohortes t ON a.mes_cohorte = t.mes_cohorte
GROUP BY a.mes_cohorte, a.mes_desde_primera_compra, t.clientes_iniciales;
