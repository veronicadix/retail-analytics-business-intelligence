# Caso 04 | E-commerce Conversion & Business Requirements

**Portafolio Retail Analytics & Business Intelligence** · Business Analysis · SQL · Google BigQuery · GA4 · BPMN · UAT

[English version](README_EN.md)

## Resumen ejecutivo

Estudio de caso basado en el dataset público y ofuscado **Google Analytics 4 E-commerce Sample** para analizar recorridos secuenciales de compra, detectar oportunidades de investigación y transformarlas en un paquete de documentación funcional: BRD, BPMN AS-IS/TO-BE, historias de usuario, criterios de aceptación y matriz UAT.

**Pregunta de negocio:** ¿En qué etapas del recorrido de compra dejan de avanzar los usuarios y qué requisitos permitirían medir y validar posibles mejoras?

> **Alcance:** análisis exploratorio y diseño funcional, no una implementación de cambios de la tienda ni una ejecución de pruebas de aceptación. Los puntos de fricción sugeridos son hipótesis, no causas verificadas.

## Datos y metodología

- **Fuente:** `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`.
- **Período:** 2020-11-01 a 2021-01-31 (92 días de cobertura observados en la exploración).
- **Herramientas:** Google BigQuery (SQL), Bizagi Modeler/BPMN 2.0, Markdown y CSV.
- **Unidad de análisis de los embudos:** usuarios con `user_pseudo_id` no nulo y eventos en orden temporal, contados una vez por etapa.
- **Embudo principal:** `view_item → add_to_cart → begin_checkout → purchase`.
- **Subembudo de checkout:** `begin_checkout → add_shipping_info → add_payment_info → purchase`.

Los embudos se calculan **independientemente**: el subembudo comienza en todos los usuarios con `begin_checkout`, sin requerir una visualización previa de producto. No exigen que los eventos pertenezcan a una misma sesión ni al mismo artículo, y pueden excluir compras realizadas mediante rutas alternativas o con eventos faltantes.

## Resultados cuantitativos

### Embudo principal (SQL 02)

| Evento | Usuarios | Conversión respecto de etapa anterior | No avanzan respecto de etapa anterior | Conversión acumulada |
|---|---:|---:|---:|---:|
| `view_item` | 61.252 | — | — | 100,00 % |
| `add_to_cart` | 12.052 | 19,68 % | 80,32 % | 19,68 % |
| `begin_checkout` | 4.909 | 40,73 % | 59,27 % | 8,01 % |
| `purchase` | 2.833 | 57,71 % | 42,29 % | **4,63 %** |

La mayor reducción de usuarios se observa entre `view_item` y `add_to_cart` (49.200 usuarios del conjunto inicial no completaron la secuencia hasta esa etapa).

### Subembudo de checkout (SQL 03)

| Evento | Usuarios | Conversión respecto de etapa anterior | No avanzan respecto de etapa anterior |
|---|---:|---:|---:|
| `begin_checkout` | 9.715 | — | — |
| `add_shipping_info` | 6.588 | 67,81 % | 32,19 % |
| `add_payment_info` | 4.334 | 65,79 % | 34,21 % |
| `purchase` | 3.320 | 76,60 % | 23,40 % |

De los 9.715 usuarios que iniciaron checkout, 3.320 completaron **esta secuencia de eventos**: conversión secuencial acumulada aproximada **34,17 %**. La mayor pérdida porcentual por transición es envío → pago (34,21 %); la mayor pérdida absoluta es checkout → envío (3.127 usuarios).

### Alerta de instrumentación

La exploración por evento (SQL 01) detectó `add_to_cart` en **74** días y `purchase` en **92** días. Esta diferencia requiere revisar cobertura e instrumentación antes de interpretar la caída únicamente como fricción UX.

## Hipótesis y oportunidades, no causas confirmadas

1. **Descubrimiento y carrito:** investigar información de producto, claridad de CTA y consistencia de instrumentación.
2. **Formulario de envío:** evaluar validaciones accesibles y telemetría de errores sin recopilar datos personales.
3. **Transición envío → pago:** analizar claridad y visibilidad de costos y pasos.
4. **Pago:** diseñar manejo seguro de errores, estado de procesamiento y reintentos sin duplicidad.
5. **Medición:** definir métricas reproducibles y alertas de calidad; validar mejoras mediante experimentos controlados.

No se dispone de datos sobre motivos de abandono, fallos de pago ni costos inesperados; cualquier mejora propuesta exige validación de UX, ingeniería y negocio.

## Entregables del proyecto

| Entregable | Archivo o ubicación |
|---|---|
| Exploración de eventos | [`sql/01_exploracion_eventos_ga4.sql`](sql/01_exploracion_eventos_ga4.sql) · [`resultados/01_exploracion_eventos_ga4.csv`](resultados/01_exploracion_eventos_ga4.csv) |
| Embudo principal | [`sql/02_funnel_conversion_ga4.sql`](sql/02_funnel_conversion_ga4.sql) · [`resultados/02_funnel_conversion_ga4.csv`](resultados/02_funnel_conversion_ga4.csv) |
| Checkout | [`sql/03_checkout_dropoff_ga4.sql`](sql/03_checkout_dropoff_ga4.sql) · [`resultados/03_checkout_dropoff_ga4.csv`](resultados/03_checkout_dropoff_ga4.csv) |
| Hallazgos de negocio | [`documentacion/04_analisis_hallazgos_comerciales.md`](documentacion/04_analisis_hallazgos_comerciales.md) |
| Business Requirements Document | [`documentacion/BRD/05_brd_ecommerce_checkout.md`](documentacion/BRD/05_brd_ecommerce_checkout.md) |
| Diagramas BPMN editables | [`documentacion/BPMN/06_bpmn_as_is_checkout.bpmn`](documentacion/BPMN/06_bpmn_as_is_checkout.bpmn) · [`documentacion/BPMN/06_bpmn_to_be_checkout.bpmn`](documentacion/BPMN/06_bpmn_to_be_checkout.bpmn) |
| Historias de usuario y criterios de aceptación | [`documentacion/historias_usuario/07_historias_usuario_criterios_aceptacion.md`](documentacion/historias_usuario/07_historias_usuario_criterios_aceptacion.md) |
| Matriz UAT | [`documentacion/UAT/08_matriz_pruebas_uat.csv`](documentacion/UAT/08_matriz_pruebas_uat.csv) · [`documentacion/UAT/08_matriz_pruebas_uat.md`](documentacion/UAT/08_matriz_pruebas_uat.md) |
| Documentación en inglés | [`README_EN.md`](README_EN.md) |

Los BPMN se pueden importar en Bizagi Modeler mediante **Importar → BPMN**. Los PNG exportados desde Bizagi pueden añadirse a `visualizaciones/` para mejorar la lectura del repositorio, sin ser requisito de la lógica SQL.

## Trazabilidad del análisis a la solución

**Datos GA4 → SQL y CSV → hallazgos → requisitos de negocio (RN) / funcionales (RF) → historias HU-01 a HU-10 → 31 escenarios UAT**.

Se diseñaron **31 casos UAT** asociados a los criterios de aceptación. **Estado: No ejecutado**; no se afirma aprobación de pruebas ni despliegue de funcionalidades.

## Reproducibilidad

1. Abrir Google BigQuery con acceso al proyecto `bigquery-public-data`.
2. Usar ubicación de procesamiento **US** para consultar la muestra pública.
3. Ejecutar, en orden, los SQL de `sql/` y contrastar sus resultados con los CSV de `resultados/`.
4. Revisar el período y las reglas de secuencia al comparar cifras. La muestra es histórica y ofuscada, por lo que puede contener inconsistencias propias del dataset.
5. Consultar el BRD y las historias para distinguir funcionalidades analizadas de propuestas pendientes de implementación.

> **Privacidad:** no incluir credenciales, datos personales, tokens ni archivos de configuración de acceso en el repositorio.

## Competencias demostradas

SQL analítico en BigQuery · análisis de eventos GA4 · diseño de métricas de conversión · análisis de calidad de datos · levantamiento y documentación de requerimientos · BPMN · historias de usuario Agile · criterios de aceptación · planificación UAT · trazabilidad funcional.

**Fuente:** [Google Analytics sample dataset for BigQuery (documentación oficial)](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset).
