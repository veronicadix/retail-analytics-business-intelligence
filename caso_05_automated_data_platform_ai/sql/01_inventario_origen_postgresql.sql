-- CASO 05 | Etapa 01 | Inventario de fuentes PostgreSQL
-- Ejecutar en la base de datos portafolio_retail.
-- Solo lectura: no crea, modifica ni elimina tablas.

SELECT 'base_movimientos' AS tabla, COUNT(*) AS total_filas
FROM public.base_movimientos
UNION ALL
SELECT 'facturas_venta', COUNT(*)
FROM public.facturas_venta
UNION ALL
SELECT 'catalogo_codigos', COUNT(*)
FROM public.catalogo_codigos;

-- Estructura disponible para diseñar la extracción y el contrato de datos.
SELECT table_name, ordinal_position, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('base_movimientos','facturas_venta','catalogo_codigos')
ORDER BY table_name, ordinal_position;
