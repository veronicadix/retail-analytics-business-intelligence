/*
Archivo: 02_estructura_objetos.sql
Etapa: 1 — Consolidación de PostgreSQL
Base de datos: portafolio_retail | Esquema: public
Objetivo: documentar nombres y tipos de columnas existentes antes de cambiar SQL.
Seguridad: consultas de lectura; no exponen registros de clientes.
Salida: inventario de columnas y conteo agregado de filas por tabla.
*/

-- 1) Confirmar en qué base de datos se ejecuta el diagnóstico.
SELECT current_database() AS base_actual;

-- 2) Listar columnas y tipos de las 3 tablas y 6 vistas confirmadas.
SELECT
    c.table_name,              -- Objeto al que pertenece la columna.
    c.ordinal_position,        -- Orden de presentación en el objeto.
    c.column_name,             -- Nombre real para futuros scripts.
    c.data_type,               -- Tipo genérico definido en PostgreSQL.
    c.udt_name,                -- Tipo subyacente (p. ej. int4, numeric, varchar).
    c.is_nullable              -- Indica si admite valores nulos.
FROM information_schema.columns AS c
WHERE c.table_schema = 'public'
  AND c.table_name IN (
      'base_movimientos', 'catalogo_codigos', 'facturas_venta',
      'vw_indicadores_producto', 'vw_perfil_clientes', 'vw_producto_mes',
      'vw_recompra_producto', 'vw_segmentos_clientes', 'vw_valor_clientes'
  )
ORDER BY c.table_name, c.ordinal_position;

-- 3) Contar registros por tabla: solo totales, sin registros personales.
SELECT 'base_movimientos' AS tabla, COUNT(*) AS total_filas
FROM public.base_movimientos
UNION ALL
SELECT 'catalogo_codigos', COUNT(*) FROM public.catalogo_codigos
UNION ALL
SELECT 'facturas_venta', COUNT(*) FROM public.facturas_venta;
