-- CASO 04: Analisis de checkout
-- Usuarios secuenciales por etapa

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
      'begin_checkout',
      'add_shipping_info',
      'add_payment_info',
      'purchase'
    )
    AND user_pseudo_id IS NOT NULL
),

checkout AS (
  SELECT
    user_pseudo_id,
    MIN(event_timestamp) AS momento
  FROM eventos
  WHERE event_name = 'begin_checkout'
  GROUP BY 1
),

shipping AS (
  SELECT
    e.user_pseudo_id,
    MIN(e.event_timestamp) AS momento
  FROM eventos e
  JOIN checkout c USING (user_pseudo_id)
  WHERE e.event_name = 'add_shipping_info'
    AND e.event_timestamp > c.momento
  GROUP BY 1
),

payment AS (
  SELECT
    e.user_pseudo_id,
    MIN(e.event_timestamp) AS momento
  FROM eventos e
  JOIN shipping s USING (user_pseudo_id)
  WHERE e.event_name = 'add_payment_info'
    AND e.event_timestamp > s.momento
  GROUP BY 1
),

purchase AS (
  SELECT
    e.user_pseudo_id,
    MIN(e.event_timestamp) AS momento
  FROM eventos e
  JOIN payment p USING (user_pseudo_id)
  WHERE e.event_name = 'purchase'
    AND e.event_timestamp > p.momento
  GROUP BY 1
),

conteos AS (
  SELECT 1 AS orden, 'begin_checkout' AS etapa,
         COUNT(*) AS usuarios FROM checkout
  UNION ALL
  SELECT 2, 'add_shipping_info', COUNT(*) FROM shipping
  UNION ALL
  SELECT 3, 'add_payment_info', COUNT(*) FROM payment
  UNION ALL
  SELECT 4, 'purchase', COUNT(*) FROM purchase
)

SELECT
  etapa,
  usuarios,
  ROUND(
    100 * SAFE_DIVIDE(
      usuarios,
      LAG(usuarios) OVER (ORDER BY orden)
    ), 2
  ) AS conversion_etapa_pct,
  ROUND(
    100 * (
      1 - SAFE_DIVIDE(
        usuarios,
        LAG(usuarios) OVER (ORDER BY orden)
      )
    ), 2
  ) AS abandono_etapa_pct
FROM conteos
ORDER BY orden;