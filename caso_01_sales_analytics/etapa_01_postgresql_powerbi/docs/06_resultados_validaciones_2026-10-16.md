# Registro consolidado de validaciones — 2026-10-16

Base: `portafolio_retail`; esquema: `public`. Evidencia: salidas agregadas compartidas de pgAdmin; **no se ejecutaron consultas desde este paquete**.

## Inventario y volumen

- Tablas: `base_movimientos` (1.033.036 filas, 19 columnas); `catalogo_codigos` (5.304 filas, 7 columnas); `facturas_venta` (39.516 filas, 10 columnas).
- Vistas: `vw_indicadores_producto`, `vw_perfil_clientes`, `vw_producto_mes`, `vw_recompra_producto`, `vw_segmentos_clientes`, `vw_valor_clientes`.
- Fechas de movimientos: 2009-12-01 07:45:00 a 2011-12-09 12:50:00.

## Calidad observada

Resultados **0** en los controles reportados: `cantidad_nula`, `factura_nula`, `fecha_nula`, `flag_abonos_fuera_0_1`, `flag_demanda_fuera_0_1`, `flag_recompra_fuera_0_1`, `flag_ventas_brutas_fuera_0_1`, `id_linea_duplicado_excedente`, `id_linea_nulo`, `importe_gbp_nulo`, `precio_gbp_nulo`, `producto_nulo`, `tipo_movimiento_nulo`; catálogo: `producto_duplicado_excedente` y `producto_nulo`; facturas: `factura_duplicada_excedente`, `factura_nula` y `fecha_factura_nula`. Estos son controles reportados, no garantía de ausencia de otros defectos.

## Reconciliación comercial (GBP sin redondear)

| Métrica | Importe |
|---|---:|
| Ventas brutas mercancía (`incluir_ventas_brutas=1`) | 19643861.637 |
| Abonos mercancía (`incluir_abonos_mercancia=1`) | -716462.57 |
| Ventas netas (suma de ambas categorías) | 18927399.067 |
| Diferencia frente a suma esperada | 0 |

## Clasificación pendiente de revisión

- Mercancía `ajuste_negativo_sin_C_revisar`: 3373 filas, importe agregado 0.
- Mercancía `precio_cero_revisar`: 2572 filas, importe agregado 0.
- Movimiento manual `cancelacion_atipica_revisar`: 1 fila, importe agregado positivo 373.57 GBP.
- Hay clases fuera de mercancía (transporte, movimiento manual, comisiones, etc.); no confundir ingresos brutos generales con ventas de mercancía.

## Próximos pendientes

1. Ejecutar `03_validaciones/05_coherencia_flags.sql`; resultado aún no recibido.
2. Conciliar `facturas_venta` contra movimientos y validar granularidad.
3. Verificar las seis vistas y las medidas Power BI; **dashboard no certificado**.
4. Documentar transformaciones originales antes de cambiarlas.
