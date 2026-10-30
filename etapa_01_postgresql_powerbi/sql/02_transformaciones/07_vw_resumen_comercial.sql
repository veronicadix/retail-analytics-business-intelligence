-- PROYECTO 1 | ETAPA 1 | V08
-- Archivo: 07_vw_resumen_comercial.sql
-- Objetivo: crear una vista de KPI globales para alimentar Power BI.
-- Fuente: public.base_movimientos (reglas ya conciliadas).
-- Impacto: crea o actualiza SOLO public.vw_resumen_comercial.
-- No modifica tablas ni las seis vistas existentes.
-- Ejecutar conectado a la base de datos portafolio_retail.

CREATE OR REPLACE VIEW public.vw_resumen_comercial AS
SELECT
    -- Una fila por conjunto completo de movimientos, antes de filtros de Power BI.
    COUNT(*) AS total_movimientos,

    -- Ventas brutas: únicamente las líneas comerciales marcadas como incluidas.
    COALESCE(SUM(importe_gbp) FILTER (WHERE incluir_ventas_brutas = 1), 0)
        AS ventas_brutas_gbp,

    -- Abonos: se preserva su signo negativo.
    COALESCE(SUM(importe_gbp) FILTER (WHERE incluir_abonos_mercancia = 1), 0)
        AS abonos_mercancia_gbp,

    -- Ventas netas: suma de las dos categorías sin doble conteo
    -- (la validación V07 confirmó que sus flags no se solapan).
    COALESCE(SUM(importe_gbp) FILTER (
        WHERE incluir_ventas_brutas = 1 OR incluir_abonos_mercancia = 1
    ), 0) AS ventas_netas_gbp,

    -- Demanda en unidades según la definición de negocio existente.
    COALESCE(SUM(cantidad) FILTER (WHERE incluir_demanda_unidades = 1), 0)
        AS unidades_vendidas,

    -- Facturas con al menos una línea de venta de mercancía.
    COUNT(DISTINCT factura) FILTER (WHERE incluir_ventas_brutas = 1)
        AS facturas_venta,

    -- Compradores identificados con compra elegible para análisis de recompra.
    COUNT(DISTINCT NULLIF(BTRIM(cliente_id), '')) FILTER (
        WHERE incluir_ventas_brutas = 1 AND incluir_recompra = 1
    ) AS clientes_compradores,

    -- Rango de fechas disponible: útil para mostrar el contexto del reporte.
    MIN(fecha) AS fecha_minima,
    MAX(fecha) AS fecha_maxima
FROM public.base_movimientos;

-- ÚNICA VERIFICACIÓN DE ESTA ENTREGA: revisar la fila calculada.
SELECT * FROM public.vw_resumen_comercial;
