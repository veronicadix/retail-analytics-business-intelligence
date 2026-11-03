# Caso 04 — Análisis de hallazgos comerciales

**Proyecto:** Retail Analytics & Business Intelligence  
**Caso:** E-commerce Conversion & Business Requirements  
**Fuente:** Google Analytics 4 — dataset público `bigquery-public-data.ga4_obfuscated_sample_ecommerce`  
**Periodo:** 2020-11-01 a 2021-01-31 (92 días)  
**Estado:** Diagnóstico preliminar, basado en tres consultas SQL.

## 1. Objetivo de negocio

Identificar los puntos con mayor pérdida de usuarios en el recorrido de compra del comercio electrónico y formular oportunidades de investigación y mejora funcional sustentadas en evidencia, para su posterior traducción a requerimientos de negocio, BPMN, historias de usuario y pruebas UAT.

## 2. Datos y evidencias

| Evidencia | Descripción |
|---|---|
| `sql/01_exploracion_eventos_ga4.sql` | Conteos de eventos, usuarios por evento y días con datos |
| `resultados/01_exploracion_eventos_ga4.csv` | Salida de la exploración |
| `sql/02_funnel_conversion_ga4.sql` | Secuencia por usuario: producto → carrito → checkout → compra |
| `resultados/02_funnel_conversion_ga4.csv` | Resultado del embudo principal |
| `sql/03_checkout_dropoff_ga4.sql` | Secuencia por usuario: checkout → envío → pago → compra |
| `resultados/03_checkout_dropoff_ga4.csv` | Resultado del subembudo de checkout |

En la exploración se observaron **17 tipos de eventos**. `add_to_cart` estuvo presente en **74 de los 92 días**; se requiere verificar la cobertura de instrumentación antes de realizar afirmaciones causales.

## 3. Embudo de conversión principal

| Etapa | Usuarios | Conversión frente a etapa anterior | Pérdida frente a etapa anterior | Conversión acumulada |
|---|---:|---:|---:|---:|
| `view_item` | 61.252 | — | — | 100,00 % |
| `add_to_cart` | 12.052 | 19,68 % | 80,32 % | 19,68 % |
| `begin_checkout` | 4.909 | 40,73 % | 59,27 % | 8,01 % |
| `purchase` | 2.833 | 57,71 % | 42,29 % | 4,63 % |

**Hallazgo H-01.** De 61.252 usuarios que registraron una visualización de producto, 12.052 completaron posteriormente el evento `add_to_cart` conforme a la secuencia implementada; **49.200 no avanzaron a esa etapa dentro de la definición de la consulta**. Esta es la mayor pérdida absoluta y relativa del embudo principal. **No equivale necesariamente a abandono de carrito**: mide la transición de visualización a adición al carrito.

**Hallazgo H-02.** De los 12.052 usuarios que llegaron secuencialmente a `add_to_cart`, 4.909 registraron posteriormente `begin_checkout`. La pérdida entre estas etapas fue de **7.143 usuarios (59,27 %)**.

**Hallazgo H-03.** De 4.909 usuarios en checkout dentro del embudo principal, 2.833 alcanzaron `purchase` secuencialmente: **57,71 %** de conversión entre las últimas dos etapas y **4,63 %** desde la primera etapa.

## 4. Subembudo de checkout

| Etapa | Usuarios | Conversión frente a etapa anterior | Pérdida frente a etapa anterior |
|---|---:|---:|---:|
| `begin_checkout` | 9.715 | — | — |
| `add_shipping_info` | 6.588 | 67,81 % | 32,19 % |
| `add_payment_info` | 4.334 | 65,79 % | 34,21 % |
| `purchase` | 3.320 | 76,60 % | 23,40 % |

**Hallazgo H-04.** La mayor pérdida absoluta del subembudo ocurre entre inicio de checkout e información de envío: **3.127 usuarios**. La mayor tasa porcentual de pérdida ocurre entre envío y pago: **34,21 % (2.254 usuarios)**.

**Hallazgo H-05.** De 9.715 usuarios que iniciaron checkout, 3.320 completaron la secuencia hasta `purchase`, equivalentes a **34,17 %**. Los **6.395** restantes no completaron *esta secuencia*, lo que no demuestra por sí solo que abandonaran definitivamente una compra.

### Por qué los dos conteos de checkout y purchase son diferentes

El embudo principal exige empezar por `view_item` y avanzar por carrito y checkout. El subembudo empieza directamente en `begin_checkout` e incluye envío y pago. **Son poblaciones y reglas de inclusión distintas**, por lo que las cifras de `begin_checkout` y `purchase` no deben mezclarse ni compararse como si provinieran del mismo embudo.

## 5. Hipótesis y oportunidades de negocio

| ID | Evidencia | Hipótesis a investigar, no confirmada | Acción propuesta |
|---|---|---|---|
| OPP-01 | H-01: 80,32 % sin progresión producto → carrito | Información de producto, precio, disponibilidad o llamada a la acción insuficiente | Revisar detalle de producto, instrumentación de eventos y pruebas de usabilidad |
| OPP-02 | H-02: 59,27 % sin progresión carrito → checkout | Sorpresas en costos o fricción al iniciar checkout | Revisar flujo, costos comunicados y requisitos de acceso |
| OPP-03 | H-04: 3.127 usuarios sin avance checkout → envío | Complejidad del formulario o validaciones poco claras | Inspeccionar campos, errores y experiencia móvil |
| OPP-04 | H-04: 34,21 % sin avance envío → pago | Fricción al pasar de envío a pago | Evaluar claridad de tarifas y disponibilidad de medios de pago |
| OPP-05 | H-04: 23,40 % sin avance pago → compra | Errores o rechazos de pago, o fallas en el seguimiento | Revisar eventos de error, respuestas de pasarela y confirmaciones |

**Priorización preliminar:** primero verificar la instrumentación y el recorrido real; después investigar OPP-01, OPP-03 y OPP-04 por el volumen de usuarios afectado. La prioridad definitiva requiere evaluación de impacto, viabilidad y esfuerzo con negocio y tecnología.

## 6. Recomendaciones funcionales para el BRD

1. Definir y documentar el contrato de eventos GA4 de cada etapa (disparador, parámetros, identificadores y criterios de éxito).
2. Instrumentar errores de formulario y errores de pago de forma agregada, sin almacenar información personal o financiera sensible.
3. Proponer mensajes de validación comprensibles y persistencia segura de datos no sensibles al avanzar por checkout.
4. Solicitar experimentos o pruebas controladas para validar las posibles mejoras antes de atribuirles efecto sobre conversiones.
5. Crear métricas estables por sesión y por usuario y segmentarlas por dispositivo, canal y fecha cuando la calidad de los datos lo permita.

## 7. Limitaciones y precauciones

- El dataset es una muestra pública histórica y ofuscada; no representa resultados comerciales actuales.
- Las consultas ordenan eventos por `user_pseudo_id` a lo largo del periodo, sin exigir la misma sesión ni el mismo producto.
- Una ausencia de evento posterior no prueba abandono definitivo, intención de compra ni causa de fricción.
- La elección del primer evento por etapa puede excluir trayectorias posteriores válidas, por ejemplo cuando un usuario vuelve a mirar productos o inicia otro checkout.
- Se requiere revisar la cobertura desigual de `add_to_cart` (74 días) y posibles diferencias entre instrumentación y comportamiento.
- No se dispone aquí de datos de ingresos atribuibles a estas rutas; no se estimará recuperación económica sin evidencia.

## 8. Próximos entregables

- `documentacion/BRD/05_brd_ecommerce_checkout.md`: contexto, alcance, requisitos, reglas de negocio, métricas de éxito, supuestos y trazabilidad.
- `documentacion/BPMN/`: diagrama AS-IS y propuesta TO-BE, claramente identificando los pasos inferidos.
- `documentacion/historias_usuario/`: historias, prioridades y criterios de aceptación.
- `documentacion/UAT/`: matriz de pruebas, datos de prueba y resultados esperados.

---

*Documento elaborado con los resultados compartidos de las consultas 01, 02 y 03. Las hipótesis requieren validación; no constituyen causas demostradas.*
