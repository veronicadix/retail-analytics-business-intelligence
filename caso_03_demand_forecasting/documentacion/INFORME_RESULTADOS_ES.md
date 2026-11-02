# Informe de resultados comerciales — Caso 03

**Tema:** Demand Forecasting & Inventory Planning  
**Naturaleza:** proyecto de portafolio con datos históricos M5 y escenarios hipotéticos de inventario  
**Prueba final:** 28 de marzo al 24 de abril de 2016

## Resumen ejecutivo
Se analizaron 30.490 series producto-tienda. Para pronosticar ventas agregadas, el promedio de las ocho semanas previas para cada día de la semana obtuvo WAPE de 5,52 %. A nivel tienda-categoría obtuvo 9,33 %, y a nivel producto-tienda 76,217 %. El 85,81 % de las series presentaba demanda intermitente o irregular intermitente según la clasificación histórica utilizada. Un método especializado, Croston-SBA, no mejoró el WAPE global producto-tienda.

Se simularon dos políticas de inventario sobre 1.183.626 unidades de demanda del período final, bajo lead time fijo de 7 días, revisión semanal e inventario inicial equivalente a 14 días de pronóstico medio. Añadir un buffer de 7 días elevó el fill rate simulado de 83,23 % a 93,55 % y redujo las unidades no atendidas de 198.529 a 76.310. A cambio, el inventario medio aumentó de 269.815 a 458.951 unidades.

## Hallazgos principales

1. **Los patrones semanales son relevantes.** El baseline estacional superó los demás métodos agregados y segmentados evaluados.
2. **La agregación oculta incertidumbre.** El WAPE granular (76,217 %) es mucho mayor que el agregado (5,52 %) y no debe compararse sin considerar la compensación de errores.
3. **La demanda intermitente es predominante.** 22.986 series intermitentes y 3.176 irregulares intermitentes afectan el desempeño a nivel producto-tienda.
4. **Más inventario mejora la atención simulada, pero tiene costo.** El buffer permite atender 122.219 unidades adicionales y requiere 189.136 unidades más de inventario medio.
5. **La decisión depende de los supuestos de costos.** El buffer mostró menor costo calculado en 13 de 16 combinaciones evaluadas; no equivale a utilidad o ahorro real.

## Diseño de la simulación

| Parámetro | Valor / tratamiento |
|---|---|
| Horizonte | 28 días (`d_1886`–`d_1913`) |
| Series | 30.490 producto-tienda |
| Pronóstico | `Dia_semana_8s` |
| Lead time | 7 días fijos |
| Revisión | Cada 7 días |
| Inventario inicial | Equivalente a 14 días del pronóstico medio por producto-tienda |
| Buffer | 0 días vs. 7 días adicionales |
| Demanda no atendida | Ventas perdidas, sin backorders |
| Proveedor / presupuesto | Capacidad ilimitada, sin restricciones |

## Resultados comparativos

| KPI | Sin buffer | Con buffer | Diferencia con buffer |
|---|---:|---:|---:|
| Demanda atendida | 985.097 | 1.107.316 | +122.219 |
| Demanda no atendida | 198.529 | 76.310 | −122.219 |
| Fill rate | 83,23 % | 93,55 % | +10,32 pp |
| Unidades ordenadas | 759.451 | 1.139.915 | +380.464 |
| Inventario final | 119.777 | 356.190 | +236.413 |
| Inventario medio | 269.815 | 458.951 | +189.136 |

## Sensibilidad económica

Se evalúa el costo total ilustrativo mediante:

`Costo_total = inventario_medio × costo_mantener_unidad_28d + demanda_no_atendida × costo_faltante_unidad`

El punto de equilibrio para el costo de faltante es:

`Costo_faltante_equilibrio = 189136 / 122219 × costo_mantener_unidad_28d ≈ 1,5475 × costo_mantener_unidad_28d`

Por ejemplo, si mantener una unidad cuesta US$1 durante 28 días, el costo de faltante tendría que superar aproximadamente US$1,5475 por unidad para justificar el buffer **según esta fórmula**.

## Limitaciones y uso adecuado

- **No son inventarios reales:** balances, órdenes, tiempos y políticas provienen de supuestos.
- **No es optimización de inventarios:** se compararon dos escenarios prefijados.
- **No se calculó rentabilidad real:** faltan compra, margen, pedido, capital, descuentos y caducidad.
- **No se demuestra desempeño operativo:** los datos disponibles son ventas, no demanda necesariamente libre de faltantes.
- **El horizonte de prueba es limitado:** extrapolar requiere más validaciones temporales y datos operativos.

## Recomendaciones de negocio

1. Mantener el baseline semanal como referencia de seguimiento para comparaciones futuras.
2. Priorizar trabajo adicional en pronósticos producto-tienda, especialmente en series intermitentes, antes de proponer órdenes de compra reales.
3. Evaluar objetivos de fill rate y costos económicos con datos propios antes de decidir el buffer.
4. Incorporar stock disponible, órdenes en tránsito, lead times observados, restricciones y rentabilidad para avanzar hacia un modelo operativo.
5. Utilizar la simulación como evidencia de pensamiento analítico, documentación funcional y análisis de escenarios, no como prueba de ahorros conseguidos.

## Evidencia técnica

Scripts `01` a `10` en `python/`; métricas y archivos JSON en `resultados/`; gráficas en `visualizaciones/`. Especialmente: `resumen_simulacion_inventario.json`, `metodologia_costos_inventario.json`, `comparacion_simulacion_inventario_28d.csv` y `umbral_costo_faltante.csv`.
