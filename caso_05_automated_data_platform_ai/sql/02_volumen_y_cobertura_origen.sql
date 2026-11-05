-- CASO 05
-- 02_volumen_y_cobertura_origen.sql

SELECT
    'base_movimientos' AS tabla,
    COUNT(*) AS total_registros,
    MIN(fecha) AS fecha_minima,
    MAX(fecha) AS fecha_maxima
FROM public.base_movimientos

UNION ALL

SELECT
    'catalogo_codigos',
    COUNT(*),
    NULL::timestamp,
    NULL::timestamp
FROM public.catalogo_codigos

UNION ALL

SELECT
    'facturas_venta',
    COUNT(*),
    MIN(fecha_factura),
    MAX(fecha_factura)
FROM public.facturas_venta;