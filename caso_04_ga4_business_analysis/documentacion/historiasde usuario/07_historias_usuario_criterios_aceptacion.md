# Caso 04 — Entregable 07: Historias de usuario y criterios de aceptación

**Proyecto:** Retail Analytics & Business Intelligence — E-commerce Conversion & Business Requirements  
**Versión:** 1.0 (propuesta funcional, no implementación)  
**Fuente:** `05_brd_ecommerce_checkout.md`, diagramas BPMN AS-IS/TO-BE y consultas GA4 01–03  
**Estado:** Historias redactadas para refinamiento; pendientes de validación con Product Owner, UX, Ingeniería, Analytics y QA.

## 1. Propósito y evidencia

El objetivo de este backlog es convertir los requerimientos del BRD en historias verificables que permitan diagnosticar fricción, mejorar la experiencia del checkout y medir el efecto de eventuales cambios. **No representa funcionalidades implementadas ni problemas de UX demostrados.**

| Hallazgo de referencia | Dato | Interpretación permitida |
|---|---:|---|
| Embudo principal: `view_item` → `add_to_cart` | 61.252 → 12.052 usuarios; 80,32 % sin avance secuencial | Priorizar investigación de producto/carrito; no afirmar abandono causal |
| Embudo principal completo | 2.833 de 61.252; 4,63 % | Conversión secuencial por usuario, no por sesión |
| Subembudo: envío → pago | 6.588 → 4.334 usuarios; 34,21 % sin avance | Investigar transición de envío a pago |
| Subembudo checkout completo | 3.320 de 9.715; 34,17 % | Denominador diferente del embudo principal; no comparar ambas tasas como equivalentes |
| Cobertura `add_to_cart` | 74 de 92 días | Verificar instrumentación antes de atribuir resultados a UX |

**Reglas metodológicas:** aplicar RB-01 a RB-07 del BRD. En especial, usar el término *no avance en la secuencia* y no mezclar cohortes; la medición a nivel de usuario no implica sesiones ni productos equivalentes.

## 2. Convención del backlog

- **HU-01 a HU-10:** identificadores únicos; **CA-HUxx-nn:** criterios de aceptación en formato Dado/Cuando/Entonces.
- Prioridad propuesta: **P0** (fundamento de medición), **P1** (diagnóstico y prueba), **P2** (mejoras de UX condicionadas a la evidencia).
- Una historia se considera **aprobada** solamente cuando Product Owner y QA validan criterios, dependencias y definición de terminado.
- Los escenarios son especificaciones y no resultados de pruebas. **UAT pendiente** se diseñará en el entregable 08.

## 3. Historias de usuario

### HU-01 — Instrumentación estándar de eventos
**Como** analista de producto, **quiero** registrar las etapas críticas del recorrido con un esquema de eventos consistente **para** reconstruir y auditar el embudo de conversión.  
**Prioridad:** P0 · **Trazabilidad:** RN-01 / RF-01 / RNF-01 / RNF-04 / RB-01, RB-02.

**Criterios de aceptación**
- **CA-HU01-01:** Dado un entorno de prueba con consentimiento válido según la política aplicable, cuando se ejecutan las acciones de producto, carrito, checkout, envío, pago y compra, entonces cada acción instrumentada genera el evento esperado con nombre, timestamp y seudónimo permitido.
- **CA-HU01-02:** Dado un evento capturado, cuando QA inspecciona su payload, entonces no contiene dirección, correo, teléfono, número de tarjeta ni información personal prohibida.
- **CA-HU01-03:** Dado un flujo de prueba de una sola acción, cuando se inspeccionan los registros, entonces no existen duplicaciones inesperadas del mismo evento; los reintentos legítimos quedan diferenciados según diseño acordado.

**Dependencias:** diccionario de eventos, políticas de consentimiento y privacidad, entorno QA.

### HU-02 — Informe reproducible de conversión
**Como** Business Analyst, **quiero** un reporte que identifique claramente el universo y la secuencia de eventos **para** analizar tasas comparables y evitar conclusiones incorrectas.  
**Prioridad:** P0 · **Trazabilidad:** RN-01 / RF-02 / RNF-04 / RB-01 a RB-04.

**Criterios de aceptación**
- **CA-HU02-01:** Dado un periodo y un embudo definidos, cuando ejecuto el reporte, entonces aparecen conteos por etapa, conversión entre etapas y acumulada, fórmula, unidad de análisis, ventana temporal y versión de consulta.
- **CA-HU02-02:** Dadas las consultas de referencia 02 y 03, cuando reproduzco las métricas sobre el mismo snapshot y las mismas reglas, entonces obtengo los conteos documentados o registro explícitamente la diferencia y su causa.
- **CA-HU02-03:** Dados dos embudos con poblaciones iniciales distintas, cuando visualizo ambos reportes, entonces se muestra una advertencia de no comparabilidad directa.
- **CA-HU02-04:** Dado un evento posterior con timestamp igual o anterior al evento anterior, cuando calculo el embudo, entonces no cuenta como avance secuencial conforme a la regla acordada.

**Dependencias:** HU-01, SQL versionado, definición del periodo y zona horaria.

### HU-03 — Alerta de cobertura e instrumentación
**Como** responsable de Analytics QA, **quiero** detectar ausencia inesperada de eventos **para** distinguir problemas de tracking de cambios en comportamiento.  
**Prioridad:** P0 · **Trazabilidad:** RN-01 / RF-03 / RB-07.

**Criterios de aceptación**
- **CA-HU03-01:** Dado un día de prueba con ausencia artificial de un evento crítico, cuando se ejecuta el control, entonces se emite una alerta con evento, fecha, condición y evidencia.
- **CA-HU03-02:** Dado un día sin actividad esperada validado por negocio, cuando se ejecuta el control, entonces no se clasifica automáticamente como incidencia sin considerar calendario y umbrales acordados.
- **CA-HU03-03:** Dado un hallazgo de cobertura, cuando se revisa el reporte, entonces se puede registrar estado, responsable y resolución.

**Dependencias:** HU-01, reglas de umbral pendientes de acuerdo, calendario operativo.

### HU-04 — Telemetría no sensible de errores de envío
**Como** analista UX, **quiero** clasificar errores del formulario de envío **para** identificar fricciones sin recolectar datos personales.  
**Prioridad:** P1 · **Trazabilidad:** RN-02 / RF-04 / RNF-01 / RB-05.

**Criterios de aceptación**
- **CA-HU04-01:** Dado un dato de prueba inválido, cuando falla la validación de envío, entonces se registra un código de error y tipo de campo previamente aprobados, sin el valor ingresado.
- **CA-HU04-02:** Dado un evento de error, cuando se inspecciona su contenido, entonces no incluye PII ni datos de pago.
- **CA-HU04-03:** Dado un conjunto de errores de prueba, cuando se genera el reporte, entonces los errores pueden agruparse por tipo y periodo sin exponer información sensible.

**Dependencias:** taxonomía de errores, revisión de privacidad y seguridad.

### HU-05 — Validación accesible del formulario de envío
**Como** comprador, **quiero** recibir mensajes claros al completar el envío **para** corregir errores sin perder información válida.  
**Prioridad:** P2 · **Trazabilidad:** RN-02 / RF-05 / RNF-02 / RB-05 / BPMN TO-BE.

**Criterios de aceptación**
- **CA-HU05-01:** Dado un campo obligatorio vacío, cuando intento continuar, entonces veo un mensaje específico junto al campo y el foco se gestiona de modo accesible.
- **CA-HU05-02:** Dado un campo inválido y otros correctos, cuando corrijo el error, entonces los demás datos válidos se conservan.
- **CA-HU05-03:** Dado un usuario que navega solo con teclado o lector de pantalla, cuando ocurre un error, entonces el mensaje puede percibirse y asociarse al campo afectado según el estándar de accesibilidad aprobado (objetivo WCAG 2.2 AA).

**Dependencias:** HU-04, diseño UX, componentes de formulario y revisión de accesibilidad.

### HU-06 — Desglose transparente del costo antes del pago
**Como** comprador, **quiero** ver subtotal, envío, impuestos y total aplicable antes de pagar **para** confirmar el importe con información comprensible.  
**Prioridad:** P2 · **Trazabilidad:** RN-03 / RF-06 / RB-05 / BPMN TO-BE.

**Criterios de aceptación**
- **CA-HU06-01:** Dado un carrito con envío e impuestos aplicables, cuando avanzo hacia pago, entonces el resumen muestra cada componente y el total de forma consistente.
- **CA-HU06-02:** Dado un componente pendiente de cálculo, cuando veo el resumen, entonces se identifica claramente como estimado y no como importe definitivo.
- **CA-HU06-03:** Dado un cambio de dirección o modalidad de envío, cuando se recalculan costos, entonces el total visible se actualiza antes de confirmar la compra.

**Dependencias:** cálculo comercial de precios, impuestos y envío; validación de Product Owner.

### HU-07 — Estado de pago y prevención de doble envío
**Como** comprador, **quiero** conocer el estado del pago y evitar solicitudes repetidas **para** no generar incertidumbre ni pedidos duplicados.  
**Prioridad:** P2 · **Trazabilidad:** RN-04 / RF-07 / RNF-03 / RNF-06 / BPMN TO-BE.

**Criterios de aceptación**
- **CA-HU07-01:** Dado un pago en procesamiento, cuando pulso de nuevo el botón de confirmar, entonces la interfaz no dispara una segunda solicitud de creación de pedido.
- **CA-HU07-02:** Dado un procesamiento terminado, cuando se recibe éxito o fallo, entonces el usuario ve un estado comprensible sin información interna del proveedor de pago.
- **CA-HU07-03:** Dada la repetición del mismo identificador de operación en backend, cuando se reciben solicitudes duplicadas, entonces se conserva una única orden conforme al contrato de idempotencia acordado.

**Dependencias:** API/backend de órdenes, proveedor de pago en sandbox, estrategia de idempotencia.

### HU-08 — Recuperación de fallas de pago
**Como** comprador, **quiero** poder reintentar de forma segura después de un fallo **para** completar mi compra sin duplicar órdenes.  
**Prioridad:** P2 · **Trazabilidad:** RN-04 / RF-08 / RNF-03 / RNF-06 / BPMN TO-BE.

**Criterios de aceptación**
- **CA-HU08-01:** Dado un pago fallido simulado, cuando la respuesta llega a la interfaz, entonces se presenta un mensaje no sensible y una acción de reintento cuando corresponde.
- **CA-HU08-02:** Dado un reintento autorizado, cuando el comprador vuelve a pagar, entonces el pedido conserva su integridad y no aparecen dos órdenes por la misma operación.
- **CA-HU08-03:** Dado un resultado incierto o timeout, cuando el usuario consulta su estado, entonces el sistema no afirma que el pago falló o tuvo éxito sin confirmación confiable.

**Dependencias:** HU-07, contrato de estados de pagos, QA de integración.

### HU-09 — Evaluación controlada de cambios de UX
**Como** Product Owner, **quiero** comparar variantes de una mejora **para** determinar si produce un efecto medible sin confundir correlación con causalidad.  
**Prioridad:** P1 · **Trazabilidad:** RN-05 / RF-09 / RB-06, RB-07.

**Criterios de aceptación**
- **CA-HU09-01:** Dadas dos variantes de prueba, cuando un usuario elegible entra en el experimento, entonces se registra asignación consistente, exposición y eventos de resultado conforme a la política de privacidad.
- **CA-HU09-02:** Dado un reporte experimental, cuando se revisan resultados, entonces se muestran población elegible, exclusiones, métricas primarias, intervalos de incertidumbre y problemas de instrumentación conocidos.
- **CA-HU09-03:** Dado un experimento propuesto, cuando se solicita aprobación, entonces existe protocolo con hipótesis, tamaño muestral a calcular, criterios de parada y monitoreo de riesgos antes de lanzarlo.

**Dependencias:** HU-01 a HU-03, autorización de experimento, análisis estadístico.

### HU-10 — Documentación BPMN trazable
**Como** analista funcional, **quiero** representar el proceso de referencia y el propuesto mediante BPMN **para** comunicar decisiones, excepciones y cambios a desarrollo y QA.  
**Prioridad:** P1 · **Trazabilidad:** RN-02 a RN-04 / RF-10 / BPMN AS-IS y TO-BE.

**Criterios de aceptación**
- **CA-HU10-01:** Dado el archivo AS-IS, cuando el equipo lo revisa, entonces queda explícito que es una reconstrucción conceptual basada en eventos GA4, no una observación completa de la operación real.
- **CA-HU10-02:** Dado el TO-BE, cuando QA revisa los caminos principales, entonces se identifican validación de envío, visualización de total, confirmación de pago y manejo de errores/reintentos.
- **CA-HU10-03:** Dado un requerimiento RF-04 a RF-08, cuando se revisa la trazabilidad, entonces puede vincularse a una actividad o decisión del TO-BE y al menos un criterio de aceptación de este backlog.

**Dependencias:** BPMN existentes, validación por Product Owner y equipo técnico.

## 4. Matriz de trazabilidad (BRD → historias → aceptación)

| Historia | Requisito BRD | Reglas / restricciones relacionadas | Evidencia de aceptación propuesta |
|---|---|---|---|
| HU-01 | RN-01 / RF-01 | RNF-01, RNF-04, RB-01–02 | CA-HU01-01 a 03 |
| HU-02 | RN-01 / RF-02 | RNF-04, RB-01–04 | CA-HU02-01 a 04 |
| HU-03 | RN-01 / RF-03 | RB-07 | CA-HU03-01 a 03 |
| HU-04 | RN-02 / RF-04 | RNF-01, RB-05 | CA-HU04-01 a 03 |
| HU-05 | RN-02 / RF-05 | RNF-02, RB-05 | CA-HU05-01 a 03 |
| HU-06 | RN-03 / RF-06 | RB-05 | CA-HU06-01 a 03 |
| HU-07 | RN-04 / RF-07 | RNF-03, RNF-06 | CA-HU07-01 a 03 |
| HU-08 | RN-04 / RF-08 | RNF-03, RNF-06 | CA-HU08-01 a 03 |
| HU-09 | RN-05 / RF-09 | RB-06–07 | CA-HU09-01 a 03 |
| HU-10 | RN-02 a RN-04 / RF-10 | BPMN AS-IS / TO-BE | CA-HU10-01 a 03 |

## 5. Priorización y orden sugerido

**Fase 1 — Fundamentos de medición (P0):** HU-01, HU-02, HU-03.  
**Fase 2 — Diagnóstico y diseño de validación (P1):** HU-04, HU-09, HU-10.  
**Fase 3 — Hipótesis de mejora por validar (P2):** HU-05, HU-06, HU-07, HU-08.

La secuencia no constituye un compromiso de implementación. Las prioridades y estimaciones de esfuerzo deben revisarse con negocio y equipo técnico.

## 6. Definition of Ready (DoR) propuesta

Una historia está lista para desarrollo cuando: (1) valor de negocio y responsable están identificados; (2) criterios de aceptación son claros y comprobables; (3) dependencias y riesgos de privacidad/seguridad han sido revisados; (4) diseños, contratos y datos de prueba necesarios están disponibles; (5) la estimación del equipo se ha acordado.

## 7. Definition of Done (DoD) propuesta

Una historia está terminada cuando: (1) implementación y revisión técnica están completas; (2) QA ejecutó pruebas relevantes y documentó resultados; (3) criterios de aceptación se cumplieron o tienen excepciones aprobadas; (4) eventos y documentación están actualizados y versionados; (5) Product Owner acepta el resultado. **Ninguna historia cumple hoy esta DoD; son artefactos de portafolio.**

## 8. Datos y ambientes para pruebas futuras

- Dataset público GA4 ofuscado: útil para consultas y diagnóstico; **no** para simular captura de eventos en una app real ni probar pagos.
- Ambiente sandbox/prototipo: necesario para pruebas de envío, validación, idempotencia y pago.
- Datos sintéticos: usar direcciones, usuarios y medios de pago ficticios autorizados; no incluir información personal real.
- Evidencia UAT a producir: ID de caso, historia y criterio asociado, precondiciones, pasos, resultado esperado/observado, estado y enlace a evidencia.

## 9. Pendientes de validación y exclusiones

- Confirmar con el equipo si `add_shipping_info` y `add_payment_info` son eventos obligatorios en todas las rutas.
- Definir umbrales de alertas, métricas de rendimiento, política de privacidad, criterios de idempotencia y alcance WCAG aplicable.
- No extrapolar resultados del dataset histórico a una tienda actual ni cuantificar ingresos recuperables sin datos adicionales.
- **Entregable 08:** matriz UAT y casos de prueba asociados a los criterios CA-HUxx-nn.

## 10. Referencias internas del repositorio

- `../BRD/05_brd_ecommerce_checkout.md`
- `../BPMN/06_bpmn_as_is_checkout.bpmn`
- `../BPMN/06_bpmn_to_be_checkout.bpmn`
- `../../sql/01_exploracion_eventos_ga4.sql`
- `../../sql/02_funnel_conversion_ga4.sql`
- `../../sql/03_checkout_dropoff_ga4.sql`
- `../../resultados/01_exploracion_eventos_ga4.csv`
- `../../resultados/02_funnel_conversion_ga4.csv`
- `../../resultados/03_checkout_dropoff_ga4.csv`

---
**Control de cambios:** v1.0 — Backlog inicial alineado a RN-01–RN-05 y RF-01–RF-10 del BRD. Redactado como propuesta funcional y no como entrega de software productivo.
