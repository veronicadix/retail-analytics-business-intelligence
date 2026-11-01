-- Completa con ceros los meses observables sin actividad, con horizonte 0..6.
-- Excluye el ultimo mes calendario del dataset por ser parcial (dic 2011).
CREATE OR REPLACE VIEW public.vw_matriz_retencion AS
WITH limite AS (
    SELECT (DATE_TRUNC('month', MAX(fecha_factura)) - INTERVAL '1 month')::date
           AS ultimo_mes_completo
    FROM public.facturas_venta
    WHERE incluir_recompra = 1
),
cohortes AS (
    SELECT DISTINCT mes_cohorte, clientes_iniciales
    FROM public.vw_cohortes_retencion
),
periodos AS (
    SELECT c.mes_cohorte, c.clientes_iniciales,
           gs.mes AS mes_desde_primera_compra
    FROM cohortes c
    CROSS JOIN limite l
    CROSS JOIN LATERAL GENERATE_SERIES(0, 6) AS gs(mes)
    WHERE (c.mes_cohorte + gs.mes * INTERVAL '1 month')::date
          <= l.ultimo_mes_completo
)
SELECT p.mes_cohorte, p.mes_desde_primera_compra,
       p.clientes_iniciales,
       COALESCE(r.clientes_activos, 0) AS clientes_activos,
       ROUND(COALESCE(r.clientes_activos, 0)::numeric
         / NULLIF(p.clientes_iniciales, 0) * 100, 2) AS retencion_pct
FROM periodos p
LEFT JOIN public.vw_cohortes_retencion r
  ON p.mes_cohorte = r.mes_cohorte
 AND p.mes_desde_primera_compra = r.mes_desde_primera_compra;
