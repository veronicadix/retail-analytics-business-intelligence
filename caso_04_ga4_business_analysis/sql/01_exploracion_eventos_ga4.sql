-- CASO 04: E-commerce Conversion
-- Etapa 01: Exploración de eventos GA4
-- Fuente: Google BigQuery Public Dataset

SELECT
    event_name,
    COUNT(*) AS total_eventos,
    COUNT(DISTINCT user_pseudo_id) AS usuarios_unicos,
    COUNT(DISTINCT event_date) AS dias_con_eventos
FROM
    `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY
    event_name
ORDER BY
    total_eventos DESC;