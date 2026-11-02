-- PROYECTO: Analítica Comercial | Base de datos: portafolio_retail
-- ETAPA 1 | PASO 4: Diagnóstico inicial de calidad
-- Solo consultas SELECT: NO modifica tablas ni vistas.
-- Ejecutar en pgAdmin conectado a portafolio_retail.
-- Cada resultado contiene objeto, control y cantidad detectada.

-- A. Evaluar identificadores obligatorios, campos comerciales y duplicados.
SELECT 'base_movimientos' AS objeto, 'total_filas' AS control, COUNT(*) AS cantidad FROM public.base_movimientos
UNION ALL SELECT 'base_movimientos', 'id_linea_nulo', COUNT(*) FROM public.base_movimientos WHERE id_linea IS NULL
UNION ALL SELECT 'base_movimientos', 'id_linea_duplicado_excedente', COALESCE(SUM(n - 1), 0) FROM (SELECT COUNT(*) AS n FROM public.base_movimientos GROUP BY id_linea HAVING COUNT(*) > 1) d
UNION ALL SELECT 'base_movimientos', 'factura_nula', COUNT(*) FROM public.base_movimientos WHERE factura IS NULL
UNION ALL SELECT 'base_movimientos', 'producto_nulo', COUNT(*) FROM public.base_movimientos WHERE producto IS NULL
UNION ALL SELECT 'base_movimientos', 'fecha_nula', COUNT(*) FROM public.base_movimientos WHERE fecha IS NULL
UNION ALL SELECT 'base_movimientos', 'cantidad_nula', COUNT(*) FROM public.base_movimientos WHERE cantidad IS NULL
UNION ALL SELECT 'base_movimientos', 'precio_gbp_nulo', COUNT(*) FROM public.base_movimientos WHERE precio_gbp IS NULL
UNION ALL SELECT 'base_movimientos', 'importe_gbp_nulo', COUNT(*) FROM public.base_movimientos WHERE importe_gbp IS NULL
UNION ALL SELECT 'base_movimientos', 'tipo_movimiento_nulo', COUNT(*) FROM public.base_movimientos WHERE tipo_movimiento IS NULL
UNION ALL SELECT 'base_movimientos', 'flag_ventas_brutas_fuera_0_1', COUNT(*) FROM public.base_movimientos WHERE incluir_ventas_brutas IS NOT NULL AND incluir_ventas_brutas NOT IN (0,1)
UNION ALL SELECT 'base_movimientos', 'flag_abonos_fuera_0_1', COUNT(*) FROM public.base_movimientos WHERE incluir_abonos_mercancia IS NOT NULL AND incluir_abonos_mercancia NOT IN (0,1)
UNION ALL SELECT 'base_movimientos', 'flag_recompra_fuera_0_1', COUNT(*) FROM public.base_movimientos WHERE incluir_recompra IS NOT NULL AND incluir_recompra NOT IN (0,1)
UNION ALL SELECT 'base_movimientos', 'flag_demanda_fuera_0_1', COUNT(*) FROM public.base_movimientos WHERE incluir_demanda_unidades IS NOT NULL AND incluir_demanda_unidades NOT IN (0,1)
UNION ALL SELECT 'catalogo_codigos', 'total_filas', COUNT(*) FROM public.catalogo_codigos
UNION ALL SELECT 'catalogo_codigos', 'producto_nulo', COUNT(*) FROM public.catalogo_codigos WHERE producto IS NULL
UNION ALL SELECT 'catalogo_codigos', 'producto_duplicado_excedente', COALESCE(SUM(n - 1), 0) FROM (SELECT COUNT(*) AS n FROM public.catalogo_codigos GROUP BY producto HAVING COUNT(*) > 1) d
UNION ALL SELECT 'facturas_venta', 'total_filas', COUNT(*) FROM public.facturas_venta
UNION ALL SELECT 'facturas_venta', 'factura_nula', COUNT(*) FROM public.facturas_venta WHERE factura IS NULL
UNION ALL SELECT 'facturas_venta', 'factura_duplicada_excedente', COALESCE(SUM(n - 1), 0) FROM (SELECT COUNT(*) AS n FROM public.facturas_venta GROUP BY factura HAVING COUNT(*) > 1) d
UNION ALL SELECT 'facturas_venta', 'fecha_factura_nula', COUNT(*) FROM public.facturas_venta WHERE fecha_factura IS NULL
ORDER BY objeto, control;

-- B. Distribución de clases y tipos para revisar reglas de negocio.
SELECT clase_codigo, tipo_movimiento, COUNT(*) AS filas,
       SUM(COALESCE(importe_gbp,0)) AS importe_total_gbp
FROM public.base_movimientos
GROUP BY clase_codigo, tipo_movimiento
ORDER BY filas DESC;

-- C. Fechas mínima/máxima para comprobar cobertura temporal.
SELECT MIN(fecha) AS fecha_minima, MAX(fecha) AS fecha_maxima
FROM public.base_movimientos;
