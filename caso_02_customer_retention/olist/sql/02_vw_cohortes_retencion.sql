-- Caso 2 / Olist | 02: cohortes por primer mes de compra
-- Solo devuelve meses con al menos un cliente activo; al agregar, completar ceros.
CREATE OR REPLACE VIEW olist.vw_cohortes_retencion AS
WITH primera_compra AS (
    SELECT customer_unique_id, MIN(mes_compra) AS mes_cohorte
    FROM olist.vw_pedidos_analiticos
    GROUP BY customer_unique_id
),
actividad_mensual AS (
    SELECT DISTINCT p.customer_unique_id, p.mes_compra, c.mes_cohorte,
           (EXTRACT(YEAR FROM AGE(p.mes_compra,c.mes_cohorte))*12
            + EXTRACT(MONTH FROM AGE(p.mes_compra,c.mes_cohorte)))::integer
             AS mes_desde_primera_compra
    FROM olist.vw_pedidos_analiticos p
    JOIN primera_compra c ON p.customer_unique_id = c.customer_unique_id
),
tamano_cohortes AS (
    SELECT mes_cohorte, COUNT(*) AS clientes_iniciales
    FROM primera_compra GROUP BY mes_cohorte
)
SELECT a.mes_cohorte, a.mes_desde_primera_compra, t.clientes_iniciales,
       COUNT(DISTINCT a.customer_unique_id) AS clientes_activos,
       ROUND(100.0*COUNT(DISTINCT a.customer_unique_id)
             /NULLIF(t.clientes_iniciales,0),2) AS retencion_pct
FROM actividad_mensual a
JOIN tamano_cohortes t ON a.mes_cohorte=t.mes_cohorte
GROUP BY a.mes_cohorte,a.mes_desde_primera_compra,t.clientes_iniciales;
