# Metodología y reglas de negocio — Caso 2

## 1. Objetivo y población

Analizar retención histórica y comportamiento de compra de clientes identificados en Online Retail II. Se usan `public.facturas_venta` para eventos elegibles de recompra y `public.vw_valor_clientes` como insumo de RFM. Las vistas dependen del modelo previamente preparado en el Caso 1.

## 2. Reglas de elegibilidad

Para cohortes e intervalos se exige `incluir_recompra = 1`, `cliente_id` no nulo ni vacío y `fecha_factura` no nula. Una factura consolidada es una compra; múltiples líneas de la misma factura no cuentan como compras adicionales. Las reglas de abonos y ventas elegibles fueron definidas previamente en el modelo del Caso 1.

## 3. RFM

- **R:** `dias_desde_ultima_compra` respecto a `fecha_corte` de `vw_valor_clientes`, con menor recencia como mejor resultado.
- **F:** `numero_compras`, número de compras históricas según la vista fuente.
- **M:** `compras_brutas_gbp` para puntuar M; `compras_netas_mercancia_gbp` para analizar contribución comercial neta.
- Las puntuaciones 1–5 se calculan mediante `NTILE(5)` y desempate por `cliente_id`. La distribución es **relativa**, y empates de valores pueden dividirse entre quintiles.
- Segmentos por prioridad de condiciones CASE: `Champions` (R≥4,F≥4,M≥4); `Loyal Customers` (R≥3,F≥4, sin Champions); `New / Potential` (R≥4,F≤2); `At Risk - High Value` (R≤2,F≥4,M≥3); `At Risk` (R≤2,F≥3, sin la regla anterior); `Hibernating` (R≤2,F≤2); demás `Needs Attention`.
- Los nombres de segmentos son **etiquetas analíticas históricas**, no diagnósticos de abandono presente.

## 4. Cohortes y retención

- Mes de cohorte: mes calendario de la primera factura válida del cliente.
- Actividad: al menos una factura válida en un mes dado; un cliente se cuenta una vez por cohorte y mes.
- Mes 0 = mes de adquisición. Retención del mes n = clientes de esa cohorte activos en ese mes / clientes iniciales de la cohorte × 100.
- **No consecutiva:** se puede contar actividad en el mes 3 aunque no haya actividad en el mes 2.
- `vw_matriz_retencion` cubre meses 0–6 y genera ceros para meses observables sin actividad; períodos posteriores al último mes completo observado quedan sin fila, no equivalen a 0%.
- El último mes completo considerado es noviembre de 2011; diciembre de 2011 está incompleto.
- Tasas agregadas: suma de clientes activos / suma de tamaños de las cohortes **elegibles para ese horizonte**. Mes 1: 23,34% (23 cohortes); mes 3: 24,98% (21); mes 6: 22,17% (18). No comparar como pérdida acumulada de una población invariable.

## 5. Intervalos y retraso

- `LAG(fecha_factura)` por cliente, orden por fecha y factura; diferencia de timestamps en días decimales.
- Resultados: 30.742 intervalos, 4.234 clientes con al menos dos compras; promedio 52,12, mediana 25,03, P75 62,08, P90 135,97 días.
- Para una alerta individual se necesitan **al menos 2 intervalos** (normalmente tres facturas elegibles).
- Si no hay suficientes intervalos: `Historial insuficiente`.
- Si la mediana calculada es ≤0: `Requiere revision`.
- Si `dias_desde_ultima_compra > GREATEST(30, intervalo_mediano_dias * 2)`: `Recompra retrasada`.
- En caso contrario: `Dentro de patron historico`.
- La regla es **exploratoria**, no un pronóstico ni una medida de abandono confirmado. Algunos intervalos muy cortos distorsionan los ratios de retraso; no priorizar por `ratio_retraso` sin análisis de sensibilidad.

## 6. Resultado de la regla final

| Estado | Clientes |
|---|---:|
| Historial insuficiente | 2.563 |
| Dentro de patron historico | 2.376 |
| Recompra retrasada | 892 |
| Requiere revision | 21 |
| **Total** | **5.852** |

Los 892 clientes con retraso suman £2.421.464,51 en compras netas históricas (desglose en README). Las cifras **no** son una estimación de ventas perdidas ni de impacto de una eventual campaña.

## 7. Riesgos y mejoras recomendadas

- Validar la idoneidad de `NTILE` frente a reglas que preserven empates; documentar los cambios de segmentación si se revisan.
- Comprobar sensibilidad de alertas al mínimo de 30 días y al factor 2, así como diferencias por país o valor comercial, antes de activar decisiones.
- Asegurar consistencia entre KPI de clientes identificados y KPI globales, cuya población puede diferir.
- Probar acciones de recuperación con grupos de control y evaluar recompra **incremental**, margen y costos antes de atribuir beneficios.
- Evitar publicar identificadores de clientes cuando no sean necesarios para demostrar el trabajo; preferir agregados o datos anonimizados.
- **Olist pendiente:** modelar de forma separada y comparar metodologías y hallazgos a nivel agregado; no unir datasets sin claves comunes.

## 8. Reproducibilidad

Los cinco scripts de `sql/` corresponden a las definiciones usadas en PostgreSQL. Orden de dependencias recomendado: `01_rfm_clientes.sql`, `02_cohortes_retencion.sql`, `03_matriz_retencion.sql`, `04_intervalos_recompra.sql`, `05_oportunidades_reactivacion.sql`; antes deben existir `facturas_venta` y `vw_valor_clientes`. El notebook analiza los extractos CSV en `datos/` y guarda las visualizaciones en `visualizaciones/`.
