# Olist Brasil — Retención de clientes y crecimiento de ingresos

**Caso 2 | Customer Retention & Revenue Growth**  
**Proyecto:** Retail Analytics & Business Intelligence  
**Tecnologías:** PostgreSQL, SQL, análisis de cohortes, RFM y segmentación comercial.

## Objetivo de negocio

Analizar la frecuencia de compra y la retención de clientes en el conjunto de datos histórico de comercio electrónico de Olist (Brasil). El propósito es detectar oportunidades de segunda compra y formular hipótesis comerciales medibles. Este análisis es independiente del conjunto **Online Retail II** incluido en el mismo Caso 2: no se combinan transacciones ni identificadores de las dos fuentes.

## Fuente y alcance

Fuente pública: [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Tablas de origen cargadas en el esquema `olist` de PostgreSQL:

| Tabla | Registros importados | Finalidad |
|---|---:|---|
| `olist.customers` | 99.441 | Identificación de comprador mediante `customer_unique_id` |
| `olist.orders` | 99.441 | Estado y fecha de los pedidos |
| `olist.order_items` | 112.650 | Valor de productos y flete por artículo |

**Población analítica:** pedidos con `order_status = 'delivered'`, fecha de compra disponible e identificador de comprador no nulo. Se consolida `order_items` por `order_id` antes de unirlo con pedidos, para evitar duplicar el conteo. Las cifras monetarias usan **reales brasileños (BRL)**; el indicador de ventas de productos excluye el flete.

**Período de compras de la vista analítica:** 15/09/2016–29/08/2018.

## Indicadores principales

| Indicador | Resultado |
|---|---:|
| Pedidos entregados analizados | 96.478 |
| Compradores únicos | 93.358 |
| Ventas históricas de productos, sin flete | R$ 13.221.498,11 |
| Valor promedio por pedido | R$ 137,04 |
| Compradores con exactamente un pedido | 90.557 |
| Compradores con dos o más pedidos | 2.801 |
| **Tasa de recompra observada** | **3,00 %** |

**Definición de recompra:** proporción de compradores únicos con al menos dos pedidos distintos entregados, sobre todos los compradores únicos con pedidos entregados en el período analizado. No mide probabilidad futura de recompra.

### Retención mensual por cohortes

La cohorte corresponde al mes de la primera compra entregada. Se cuenta un comprador como retenido en el mes *M+n* si efectuó al menos un pedido entregado en ese mes calendario relativo. El mes 0 es 100 % por definición. Los meses sin compradores activos se tratan como cero en la consolidación.

| Indicador | M1 | M3 | M6 |
|---|---:|---:|---:|
| Cohortes elegibles | 21 | 19 | 16 |
| Clientes iniciales de cohortes elegibles | 81.265 | 68.881 | 49.237 |
| Clientes retenidos | 390 | 180 | 116 |
| **Retención ponderada** | **0,48 %** | **0,26 %** | **0,24 %** |

**Control de madurez:** se utiliza julio de 2018 como último mes calendario completo de seguimiento; agosto de 2018 se excluye para evitar comparar meses parcialmente observados. Las cifras de M1, M3 y M6 tienen distintas poblaciones elegibles y **no** representan una secuencia de supervivencia de un mismo grupo fijo. No son métricas acumuladas.

### Variables RFM

| Variable | Resultado promedio |
|---|---:|
| Clientes analizados | 93.358 |
| Recencia | 238,48 días |
| Frecuencia | 1,03 pedidos |
| Valor monetario histórico | R$ 141,62 por cliente |

La recencia se calcula contra el día siguiente a la última fecha de compra registrada, **no contra la fecha actual**. El valor monetario suma precios de productos sin flete.

### Segmentación comercial basada en reglas

Dada la concentración de compradores de una única compra, se prefirió una clasificación interpretable basada en frecuencia y recencia, en lugar de percentiles de frecuencia poco discriminativos. El umbral de **90 días** es exploratorio, no un plazo de abandono validado estadísticamente.

| Segmento | Compradores | Participación | Valor histórico de productos |
|---|---:|---:|---:|
| Compra única antigua | 72.778 | 77,96 % | R$ 10.035.714,16 |
| Primera compra reciente | 17.779 | 19,04 % | R$ 2.457.375,20 |
| Recurrentes antiguos | 2.190 | 2,35 % | R$ 563.538,66 |
| Recurrentes recientes | 611 | 0,65 % | R$ 164.870,09 |
| **Total** | **93.358** | **100 %** | **R$ 13.221.498,11** |

**Importante:** “reciente” y “antiguo” son etiquetas respecto al cierre **histórico** del dataset. No describen el estado actual de clientes reales.

## Interpretación comercial y recomendaciones

1. **Segunda compra:** la elevada proporción de compradores con un solo pedido (97,00 %) justifica investigar el recorrido poscompra y probar incentivos controlados para compradores de primera compra reciente.
2. **Reactivación:** evaluar campañas piloto diferenciadas para compradores recurrentes históricos con recencia superior a 90 días, antes de establecer criterios definitivos de inactividad.
3. **Medición:** evaluar experimentos por incremento de recompra, margen incremental y costo de intervención; los importes históricos por segmento **no** son ingresos recuperables estimados.
4. **Profundización:** incorporar categorías de producto y calendario promocional para entender si la frecuencia esperada difiere según tipo de compra.

No es posible atribuir causalidad a la baja recompra observada solo con este análisis descriptivo. Las posibles estrategias son **hipótesis** que requieren experimentación.

## Comparación metodológica con Online Retail II

| Indicador | Online Retail II | Olist |
|---|---:|---:|
| Compradores analizados | 5.852 | 93.358 |
| Compradores recurrentes | 4.234 | 2.801 |
| Tasa de recompra observada | 72,35 % | 3,00 % |
| Retención M1 | 23,34 % | 0,48 % |
| Retención M3 | 24,98 % | 0,26 % |
| Retención M6 | 22,17 % | 0,24 % |

Esta tabla es una **comparación descriptiva, no un benchmark de desempeño**. Online Retail II usa reglas de negocio específicas (`incluir_recompra = 1`), mientras que Olist filtra pedidos entregados. Los negocios, períodos, modelos operativos y poblaciones son diferentes. Las metodologías de cohortes y elegibilidad deben considerarse antes de cualquier comparación causal o de efectividad comercial.

## Estructura SQL y reproducibilidad

Los scripts se encuentran en [`../sql/`](../sql/):

1. `00_estructura_olist.sql` — estructura de tablas.
2. `01_vw_pedidos_analiticos.sql` — una fila por pedido entregado y agregados de artículos.
3. `02_vw_cohortes_retencion.sql` — cohortes mensuales.
4. `03_vw_rfm_y_segmentos.sql` — variables RFM y segmentación.
5. `04_consultas_indicadores_olist.sql` — consultas de indicadores.
6. `05_comparacion_online_retail_ii.sql` — comparación descriptiva de recompra.

Para reproducir el análisis, descarga los CSV desde Kaggle, crea las tablas y carga los archivos en PostgreSQL antes de ejecutar las vistas en orden. Los archivos fuente originales **no se publican** en este repositorio. Revisa las reglas de cada script antes de ejecutarlo y consulta [`../sql/`](../sql/) para el SQL exacto versionado.

## Limitaciones

- Dataset histórico, no información comercial en tiempo real.
- Se consideran pedidos entregados, sin inferir devoluciones posteriores o margen comercial.
- No hay exposición de campañas, causalidad ni rentabilidad neta por cliente.
- Los umbrales de recencia son heurísticos.
- La observación de cohortes recientes está censurada por la fecha final de los datos.

**Uso:** proyecto de portafolio con fines educativos y de demostración profesional de Business Intelligence, SQL y análisis de clientes.
