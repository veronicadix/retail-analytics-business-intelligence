# V08 — Modelo existente y siguiente implementación

Fecha: 2026-10-16 · Base: `portafolio_retail` · Fuente: definiciones SQL compartidas por la usuaria.

## Seis vistas existentes (sin modificaciones)

| Vista | Uso | Base / dependencias |
|---|---|---|
| `vw_indicadores_producto` | Ventas, abonos, facturas, clientes y unidades por producto | `base_movimientos`, `catalogo_codigos` |
| `vw_producto_mes` | Ventas, abonos, unidades y facturas por producto/mes | `base_movimientos` |
| `vw_recompra_producto` | Clientes compradores y recurrentes por producto | `base_movimientos` |
| `vw_perfil_clientes` | Recencia, frecuencia y ticket de cliente | `facturas_venta` |
| `vw_valor_clientes` | Valor bruto, abonos y valor neto por cliente | `vw_perfil_clientes`, `base_movimientos` |
| `vw_segmentos_clientes` | Segmentación por valor, recencia, frecuencia y devoluciones | `vw_valor_clientes` |

## Revisión de lógica: decisiones concretas

- **No recrear ni cambiar las seis vistas**: aportan la base del dashboard.
- La conciliación global ya aprobada fue: bruto `19643861.637`, abonos `-716462.57`, neto `18927399.067` GBP.
- `vw_segmentos_clientes` usa constantes `2171.93` GBP y `96` días. **Pendiente documentar cómo se determinaron**, antes de presentar estos segmentos como criterio estable. No es un bloqueo para la vista KPI.
- `vw_valor_clientes` asigna abonos por `cliente_id`, no por factura. Es una decisión metodológica; debe explicarse en el dashboard cuando se comparen compras y abonos por cliente.
- En `vw_indicadores_producto` y `vw_producto_mes`, los resultados netos provienen de filas filtradas por los indicadores de inclusión, lo cual es consistente con las cifras conciliadas.

## Implementación V08

Archivo: `sql/02_transformaciones/07_vw_resumen_comercial.sql`.

Crea solo la vista **nueva** `public.vw_resumen_comercial`, para una fuente de KPI globales en Power BI.
Devuelve una sola fila con ventas brutas, abonos, ventas netas, unidades, facturas, compradores y rango de fechas.
**Precaución:** al ser una sola fila, no debe usarse para KPI que deban responder a filtros de producto o fecha. Para tarjetas dinámicas en Power BI, calcular las medidas desde `base_movimientos` como hasta ahora.

## Siguiente paso

1. Ejecutar el SQL de V08 una sola vez en pgAdmin contra `portafolio_retail`.
2. Compartir la fila resultante.
3. Ajustar conexión/medidas del dashboard con las vistas existentes y decidir si se utiliza la vista de KPIs para validación global.

No se requieren más chequeos genéricos de nulos o duplicados: ya están superados.
