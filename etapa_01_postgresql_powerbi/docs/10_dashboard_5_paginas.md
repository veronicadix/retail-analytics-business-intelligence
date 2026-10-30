# V10 — Dashboard comercial Power BI

Estado: **cinco páginas funcionales**, no se ha terminado el rediseño estético ni el módulo de pronósticos con incertidumbre. Fuente de verdad: captura de pantallas y resultados comunicados durante la implementación; no se adjuntó un PBIX para inspección automática.

| Página | Objetos implementados | Fuentes principales |
|---|---|---|
| Resumen comercial | 6 KPI y evolución mensual de ventas/abonos | `base_movimientos`, calendario |
| Prioridad de productos | Top 10 ventas, ABC, tabla ranking, Top 10 recompra (>=20 compradores) | `vw_indicadores_producto`, `vw_pareto_productos`, `vw_recompra_producto` |
| Clientes y retención | KPI clientes, recurrentes, ticket; 6 segmentos, Top 10 neto, tabla y segmentador | `vw_perfil_clientes`, `vw_valor_clientes`, `vw_segmentos_clientes`, `facturas_venta` |
| Evolución y planificación | Unidades mensuales 2009–2011, series 2010/2011, variaciones interanuales | `vw_producto_mes` |
| Calidad y metodología | KPI de conteo, duplicados, fechas nulas; matriz de clase/tipo e informe de metodología | `base_movimientos` |

## Notas de implementación
- En Power BI la tabla puede aparecer como `'public vw_producto_mes'` (con espacio), no como el nombre SQL con punto.
- La columna calculada de comparación se llama exactamente **`Año_Comparacion`**.
- Los porcentajes `participacion_pct`, `acumulado_pct` de ABC son números en escala 0–100; no se deben sumar para obtener un total acumulado.
- Pareto solo contempla productos con ventas netas positivas. Gráfico de recompra: mínimo 20 clientes compradores.
- Diciembre 2011 contiene datos hasta el 09/12; la variación anual completa no es directamente comparable.
- El +0,02 % comparable fue informado por la tarjeta; validar sus filtros de segmentadores/modelo si se usa en conclusiones o publicación.
- Pronóstico cuantitativo con backtesting e incertidumbre: **pendiente**, no presentar como completado.
- Las medidas adicionales que ya existían en el PBIX pero cuya fórmula no se proporcionó **no están reproducidas** aquí; la versión definitiva se puede exportar desde Power BI.
