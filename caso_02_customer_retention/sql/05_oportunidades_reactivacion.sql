-- Regla EXPLORATORIA: recencia > max(30 dias, 2 * mediana intervalos).
-- No indica abandono ni ingresos recuperables garantizados.
CREATE OR REPLACE VIEW public.vw_oportunidades_reactivacion AS
WITH intervalos_cliente AS (
    SELECT cliente_id,
           COUNT(*) AS intervalos_observados,
           ROUND(AVG(dias_entre_compras), 2) AS intervalo_promedio_dias,
           ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP
             (ORDER BY dias_entre_compras))::numeric, 2) AS intervalo_mediano_dias
    FROM public.vw_intervalos_recompra
    GROUP BY cliente_id
)
SELECT r.cliente_id, r.segmento_rfm, r.dias_desde_ultima_compra,
       r.numero_compras, r.compras_netas_mercancia_gbp,
       i.intervalos_observados, i.intervalo_promedio_dias,
       i.intervalo_mediano_dias,
       ROUND(r.dias_desde_ultima_compra::numeric
             / NULLIF(i.intervalo_mediano_dias, 0), 2) AS ratio_retraso,
       CASE
           WHEN i.intervalos_observados IS NULL OR i.intervalos_observados < 2
                THEN 'Historial insuficiente'
           WHEN i.intervalo_mediano_dias <= 0 THEN 'Requiere revision'
           WHEN r.dias_desde_ultima_compra >
                GREATEST(30, i.intervalo_mediano_dias * 2)
                THEN 'Recompra retrasada'
           ELSE 'Dentro de patron historico'
       END AS estado_recompra
FROM public.vw_rfm_clientes r
LEFT JOIN intervalos_cliente i ON r.cliente_id = i.cliente_id;
