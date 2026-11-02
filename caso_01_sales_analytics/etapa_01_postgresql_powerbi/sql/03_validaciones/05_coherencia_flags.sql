-- PROYECTO: Analítica comercial | ETAPA 1 | Validación 05
-- Base: portafolio_retail | Origen: public.base_movimientos
-- Objetivo: revisar solapamientos y coherencia de flags frente a movimientos.
-- Solo lectura: no modifica los datos.

SELECT
    -- Cuenta las líneas marcadas simultáneamente como venta y abono.
    COUNT(*) FILTER (
        WHERE incluir_ventas_brutas = 1 AND incluir_abonos_mercancia = 1
    ) AS lineas_con_ambos_flags,

    -- Detecta ventas marcadas con importes no positivos.
    COUNT(*) FILTER (
        WHERE incluir_ventas_brutas = 1 AND importe_gbp <= 0
    ) AS ventas_con_importe_no_positivo,

    -- Detecta abonos marcados con importe no negativo.
    COUNT(*) FILTER (
        WHERE incluir_abonos_mercancia = 1 AND importe_gbp >= 0
    ) AS abonos_con_importe_no_negativo,

    -- Señala filas marcadas para venta/abono fuera de la clase mercancía.
    COUNT(*) FILTER (
        WHERE (incluir_ventas_brutas = 1 OR incluir_abonos_mercancia = 1)
          AND clase_codigo IS DISTINCT FROM 'mercancia'
    ) AS flags_comerciales_fuera_mercancia,

    -- Suma importes de las filas con los dos flags activados (si existen).
    COALESCE(SUM(importe_gbp) FILTER (
        WHERE incluir_ventas_brutas = 1 AND incluir_abonos_mercancia = 1
    ), 0) AS importe_solapado_gbp
FROM public.base_movimientos;
