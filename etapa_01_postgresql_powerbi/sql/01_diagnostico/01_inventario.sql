/*
Archivo: 01_inventario.sql
Etapa: 1 — Diagnóstico PostgreSQL
Objetivo: confirmar estructura y volumen sin extraer registros personales.
Dependencias: esquema public, tablas base_movimientos, facturas_venta, catalogo_codigos.
Uso: ejecutar en pgAdmin; copiar SOLO resultados agregados a la bitácora.
*/

-- 1. Verificar existencia de las tablas esperadas.
SELECT
    t.table_schema,                                  -- Esquema donde reside la tabla.
    t.table_name                                      -- Nombre físico de la tabla.
FROM information_schema.tables AS t
WHERE t.table_schema = 'public'                      -- Limita al esquema de trabajo.
  AND t.table_name IN ('base_movimientos', 'facturas_venta', 'catalogo_codigos')
ORDER BY t.table_name;

-- 2. Inventariar columnas y tipos (sin leer valores).
SELECT
    c.table_name,                                     -- Tabla propietaria de la columna.
    c.ordinal_position,                               -- Orden de la columna en la tabla.
    c.column_name,                                    -- Nombre técnico real.
    c.data_type,                                      -- Tipo SQL declarado.
    c.is_nullable                                     -- Permite o no valores NULL.
FROM information_schema.columns AS c
WHERE c.table_schema = 'public'
  AND c.table_name IN ('base_movimientos', 'facturas_venta', 'catalogo_codigos')
ORDER BY c.table_name, c.ordinal_position;

-- 3. Conteo por tabla; son consultas agregadas sin mostrar clientes.
SELECT 'base_movimientos' AS tabla, COUNT(*) AS filas FROM public.base_movimientos
UNION ALL
SELECT 'facturas_venta', COUNT(*) FROM public.facturas_venta
UNION ALL
SELECT 'catalogo_codigos', COUNT(*) FROM public.catalogo_codigos;
