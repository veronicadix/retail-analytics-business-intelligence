/*
Archivo: 01_reconciliacion.sql
Etapa: 1 — Conciliación financiera PostgreSQL / Power BI
Objetivo: comparar ventas brutas, abonos y ventas netas usando los flags existentes.
Dependencias CONFIRMADAS: public.base_movimientos(
    importe_gbp, incluir_ventas_brutas, incluir_abonos_mercancia
).
Supuesto a verificar: importe_gbp es numérico y abonos se almacenan con signo negativo.
No modificar tablas: SELECT de solo lectura.
*/

WITH totales AS (
    SELECT
        -- Solo operaciones marcadas para ventas brutas.
        COALESCE(SUM(importe_gbp) FILTER (WHERE incluir_ventas_brutas = 1), 0) AS ventas_brutas_gbp,
        -- Se conserva el signo original de los abonos (normalmente negativo).
        COALESCE(SUM(importe_gbp) FILTER (WHERE incluir_abonos_mercancia = 1), 0) AS abonos_gbp
    FROM public.base_movimientos
)
SELECT
    ROUND(ventas_brutas_gbp::numeric, 2) AS ventas_brutas_gbp,
    ROUND(abonos_gbp::numeric, 2) AS abonos_gbp,
    -- Neto = bruto + abonos negativos; NO restar un abono ya negativo.
    ROUND((ventas_brutas_gbp + abonos_gbp)::numeric, 2) AS ventas_netas_gbp
FROM totales;

-- Comprobación de nulos en campos críticos para calcular las métricas.
SELECT
    COUNT(*) AS filas_totales,
    COUNT(*) FILTER (WHERE importe_gbp IS NULL) AS importe_nulo,
    COUNT(*) FILTER (WHERE incluir_ventas_brutas IS NULL) AS bandera_ventas_nula,
    COUNT(*) FILTER (WHERE incluir_abonos_mercancia IS NULL) AS bandera_abonos_nula,
    COUNT(*) FILTER (WHERE incluir_ventas_brutas = 1 AND incluir_abonos_mercancia = 1)
        AS doble_clasificacion_ventas_abonos
FROM public.base_movimientos;
