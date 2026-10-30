/*
Archivo: 03_resumen_columnas.sql
Etapa: 1 — Diagnóstico del esquema
Base esperada: portafolio_retail
Objetivo: obtener nombres, tipos y nulabilidad de las columnas de las 3 tablas base.
Seguridad: solo lectura; no expone datos personales ni modifica objetos.
Uso: ejecutar en pgAdmin conectado a portafolio_retail y exportar resultado.
*/

-- 1. Identificar la base en la que está conectada la sesión.
SELECT current_database() AS base_actual;

-- 2. Leer el catálogo de columnas (no las filas comerciales).
SELECT
    c.table_name AS tabla,                   -- Tabla de origen.
    c.ordinal_position AS orden_columna,     -- Posición física de la columna.
    c.column_name AS columna,                -- Nombre exacto a utilizar en scripts posteriores.
    c.data_type AS tipo_dato,                -- Tipo de dato lógico.
    c.is_nullable AS admite_nulos            -- YES: permite NULL; NO: restricción NOT NULL.
FROM information_schema.columns AS c
WHERE c.table_schema = 'public'             -- Limitar a esquema del proyecto.
  AND c.table_name IN (                      -- Solo las 3 tablas confirmadas.
      'base_movimientos',
      'catalogo_codigos',
      'facturas_venta'
  )
ORDER BY c.table_name, c.ordinal_position;  -- Resultados en orden reproducible.
