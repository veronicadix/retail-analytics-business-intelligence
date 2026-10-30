-- PROYECTO: Analítica comercial | ETAPA 1 | Paso 6
-- Base: portafolio_retail
-- Objetivo: extraer las definiciones SQL de las seis vistas existentes.
-- Uso: ejecutar en pgAdmin y exportar la tabla de resultados a CSV o copiar
-- las definiciones para documentar las transformaciones existentes.
-- Solo lectura: NO crea, modifica ni elimina objetos.

SELECT
    v.viewname AS nombre_vista,            -- Identificador de la vista.
    v.definition AS definicion_sql         -- Consulta que define la vista.
FROM pg_catalog.pg_views AS v
WHERE v.schemaname = 'public'               -- Solo esquema comercial.
  AND v.viewname IN (
      'vw_indicadores_producto',
      'vw_perfil_clientes',
      'vw_producto_mes',
      'vw_recompra_producto',
      'vw_segmentos_clientes',
      'vw_valor_clientes'
  )
ORDER BY v.viewname;                        -- Orden estable para revisión.
