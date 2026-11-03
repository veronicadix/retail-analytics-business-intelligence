-- CASO 04: E-commerce Conversion
-- Etapa 02: Embudo secuencial por usuario
-- Periodo: noviembre 2020 - enero 2021

WITH eventos AS (
  SELECT
    user_pseudo_id,
    event_name,
    event_timestamp
  FROM
    `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE
    _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
    AND event_name IN (
      'view_item',
      'add_to_cart',
      'begin_checkout',
      'purchase'
    )
    AND user_pseudo_id IS NOT NULL
),

etapa_1 AS (
  SELECT
    user_pseudo_id,
    MIN(event_timestamp) AS momento
  FROM eventos
  WHERE event_name = 'view_item'
  GROUP BY user_pseudo_id
),

etapa_2 AS (
  SELECT
    e.user_pseudo_id,
    MIN(e.event_timestamp) AS momento
  FROM eventos e
  JOIN etapa_1 a USING (user_pseudo_id)
  WHERE e.event_name = 'add_to_cart'
    AND e.event_timestamp > a.momento
  GROUP BY e.user_pseudo_id
),

etapa_3 AS (
  SELECT
    e.user_pseudo_id,
    MIN(e.event_timestamp) AS momento
  FROM eventos e
  JOIN etapa_2 a USING (user_pseudo_id)
  WHERE e.event_name = 'begin_checkout'
    AND e.event_timestamp > a.momento
  GROUP BY e.user_pseudo_id
),

etapa_4 AS (
  SELECT
    e.user_pseudo_id,
    MIN(e.event_timestamp) AS momento
  FROM eventos e
  JOIN etapa_3 a USING (user_pseudo_id)
  WHERE e.event_name = 'purchase'
    AND e.event_timestamp > a.momento
  GROUP BY e.user_pseudo_id
),

conteos AS (
  SELECT 1 AS orden, 'view_item' AS etapa,
         COUNT(*) AS usuarios FROM etapa_1
  UNION ALL
  SELECT 2, 'add_to_cart', COUNT(*) FROM etapa_2
  UNION ALL
  SELECT 3, 'begin_checkout', COUNT(*) FROM etapa_3
  UNION ALL
  SELECT 4, 'purchase', COUNT(*) FROM etapa_4
)

SELECT
  etapa,
  usuarios,
  ROUND(
    SAFE_DIVIDE(
      usuarios,
      LAG(usuarios) OVER (ORDER BY orden)
    ) * 100, 2
  ) AS conversion_etapa_pct,
  ROUND(
    (1 - SAFE_DIVIDE(
      usuarios,
      LAG(usuarios) OVER (ORDER BY orden)
    )) * 100, 2
  ) AS abandono_etapa_pct,
  ROUND(
    SAFE_DIVIDE(
      usuarios,
      FIRST_VALUE(usuarios) OVER (ORDER BY orden)
    ) * 100, 2
  ) AS conversion_acumulada_pct
FROM conteos
ORDER BY orden;