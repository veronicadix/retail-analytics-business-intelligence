-- Caso 2 - Customer Retention & Revenue Growth
-- Fuente: public.vw_valor_clientes (Caso 1)
-- RFM basado en quintiles NTILE(5). Desempate por cliente_id.
-- El valor monetario del score utiliza compras BRUTAS, tal como la vista original.
CREATE OR REPLACE VIEW public.vw_rfm_clientes AS
WITH puntuaciones AS (
    SELECT
        cliente_id, fecha_corte, primera_compra, ultima_compra,
        dias_desde_ultima_compra, numero_compras,
        compras_brutas_gbp, compras_netas_mercancia_gbp,
        abonos_mercancia_gbp,
        NTILE(5) OVER (ORDER BY dias_desde_ultima_compra DESC, cliente_id) AS r_score,
        NTILE(5) OVER (ORDER BY numero_compras ASC, cliente_id) AS f_score,
        NTILE(5) OVER (ORDER BY compras_brutas_gbp ASC, cliente_id) AS m_score
    FROM public.vw_valor_clientes
    WHERE cliente_id IS NOT NULL AND TRIM(cliente_id) <> ''
)
SELECT
    *,
    CONCAT(r_score, f_score, m_score) AS rfm_codigo,
    r_score + f_score + m_score AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New / Potential'
        WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 3 THEN 'At Risk - High Value'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Hibernating'
        ELSE 'Needs Attention'
    END AS segmento_rfm
FROM puntuaciones;
