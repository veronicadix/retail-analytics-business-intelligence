# BRD — Optimización del recorrido de compra e-commerce

**ID:** BRD-C04-001  
**Versión:** 1.0 — propuesta para portafolio  
**Proyecto:** Retail Analytics & Business Intelligence  
**Caso:** 04 — E-commerce Conversion & Business Requirements  
**Estado:** Borrador funcional para revisión (no aprobado por un negocio real)  
**Origen de datos:** `bigquery-public-data.ga4_obfuscated_sample_ecommerce`  
**Periodo de análisis:** 2020-11-01 a 2021-01-31 (92 días)  
**Responsable del documento:** Analista de negocio (proyecto de portafolio)

## 1. Resumen ejecutivo

El análisis exploratorio de eventos de Google Analytics 4 (GA4) identifica oportunidades para investigar las pérdidas de continuidad en la navegación de producto y el proceso de checkout. En un **embudo secuencial por usuario**, de 61.252 usuarios con `view_item`, 12.052 registraron posteriormente `add_to_cart` y 2.833 completaron la secuencia hasta `purchase` (conversión acumulada del **4,63 %**, según la definición de consulta). Por separado, en un **subembudo que parte de todos los usuarios con `begin_checkout`**, 9.715 iniciaron checkout y 3.320 completaron la secuencia checkout → envío → pago → compra (conversión acumulada del **34,17 %**).

**Problema de negocio:** no se dispone todavía de evidencia suficiente para explicar qué impide que parte de los usuarios continúe a las siguientes etapas ni para distinguir fricción de experiencia, fallas de instrumentación y recorridos alternativos. Se propone mejorar la **observabilidad del embudo** y diseñar intervenciones de UX sujetas a validación, antes de prometer un aumento de conversión.

**Decisión propuesta:** priorizar un diagnóstico de instrumentación y comportamiento, seguido de la validación y experimentación controlada de mejoras en ficha de producto, captura de envío y transición a pago.

## 2. Contexto y evidencia

### 2.1 Embudo principal — secuencia por usuario

| Etapa | Usuarios | Conversión vs. etapa previa | Pérdida vs. etapa previa | Conversión acumulada |
|---|---:|---:|---:|---:|
| `view_item` | 61.252 | — | — | 100,00 % |
| `add_to_cart` | 12.052 | 19,68 % | 80,32 % | 19,68 % |
| `begin_checkout` | 4.909 | 40,73 % | 59,27 % | 8,01 % |
| `purchase` | 2.833 | 57,71 % | 42,29 % | 4,63 % |

La pérdida entre `view_item` y `add_to_cart` es de **49.200 usuarios** que no completaron esa transición bajo la lógica de la consulta. No significa que todos hayan abandonado una intención de compra.

### 2.2 Subembudo de checkout — secuencia por usuario

| Etapa | Usuarios | Conversión vs. etapa previa | Pérdida vs. etapa previa |
|---|---:|---:|---:|
| `begin_checkout` | 9.715 | — | — |
| `add_shipping_info` | 6.588 | 67,81 % | 32,19 % |
| `add_payment_info` | 4.334 | 65,79 % | 34,21 % |
| `purchase` | 3.320 | 76,60 % | 23,40 % |

Pérdidas absolutas por transición: **3.127** (inicio → envío), **2.254** (envío → pago) y **1.014** (pago → compra). El **34,17 %** corresponde a 3.320 / 9.715. El subembudo parte de todos los usuarios que iniciaron checkout y **no** es una continuación directa de la población de 4.909 del embudo principal; las cifras de ambos análisis **no deben conciliarse como si fueran una única cohorte**.

### 2.3 Alerta de calidad

En la exploración, el evento `add_to_cart` aparece en **74 de 92 días**, mientras `view_item`, `begin_checkout` y `purchase` aparecen en 92. Esto requiere revisar cobertura de captura y posibles cambios de instrumentación, antes de atribuir diferencias únicamente a comportamiento del usuario.

### 2.4 Limitaciones metodológicas

- Dataset de muestra público, histórico y ofuscado; no representa la operación actual de una compañía.
- Las consultas se basan en `user_pseudo_id` y orden de `event_timestamp`, sin exigir una misma sesión ni un mismo producto.
- La lógica utiliza el primer evento admisible de cada etapa; puede excluir recorridos alternativos o eventos legítimos que no cumplan el orden impuesto.
- No se han medido causas de abandono, errores de formulario, medios de pago, costos de envío, tiempos de carga ni ventas recuperables.
- Una pérdida de avance en una secuencia **no equivale** automáticamente a abandono real, fallo de UX o ingreso perdido.

## 3. Objetivos

**OBJ-01 — Visibilidad confiable:** establecer una definición documentada y reproducible del embudo, con controles de calidad de eventos y segmentación por dispositivo, sesión y periodo cuando los datos lo permitan.

**OBJ-02 — Diagnóstico:** localizar transiciones de menor continuidad y producir hipótesis verificables sobre las causas, sin inferirlas a partir de conteos agregados.

**OBJ-03 — Mejora funcional:** proponer y validar mejoras de experiencia en ficha de producto, envío y pago con requisitos verificables.

**OBJ-04 — Medición:** definir criterios de éxito y un plan de experimentación previo a cualquier afirmación de impacto comercial.

## 4. Alcance

**Incluye (propuesta):** diccionario de eventos y métricas, controles de instrumentación, tablero de embudo, visibilidad de errores de formulario, mensajes de validación, desglose de costos antes del pago, estados claros de confirmación y un plan de pruebas/experimentos.

**Excluye:** implementación real en un sitio productivo, cambio de pasarela de pagos, rediseño integral del catálogo, desarrollo de integraciones logísticas, captura de datos personales reales, atribución causal sin experimento y proyecciones de ingresos no sustentadas.

## 5. Stakeholders y responsabilidades propuestos

| Rol (hipotético) | Necesidad / responsabilidad |
|---|---|
| Product Owner e-commerce | Priorizar objetivos y aceptar funcionalidades |
| Business Analyst | Mantener BRD, reglas, trazabilidad e historias de usuario |
| UX / Research | Validar hipótesis con observación y pruebas de usabilidad |
| Engineering / Front-end | Estimar y desarrollar cambios del flujo |
| Data / Analytics | Diseñar instrumentación, validar eventos y métricas |
| QA | Ejecutar casos de prueba y UAT con Product Owner |
| Legal / Privacy | Revisar tratamientos de datos y consentimiento si aplica |

*Estos roles son supuestos de un escenario profesional, no personas ni aprobaciones reales.*

## 6. Requerimientos de negocio

| ID | Requerimiento de negocio | Prioridad | Evidencia / motivación |
|---|---|---|---|
| RN-01 | Poder medir el avance de usuarios entre las etapas de compra mediante una definición única y auditable | Alta | Diferencias entre embudos y limitaciones de secuencia |
| RN-02 | Identificar errores y fricciones de interacción sin almacenar información sensible | Alta | Causas de pérdida actualmente desconocidas |
| RN-03 | Presentar información de envío y costos de forma comprensible antes de continuar al pago | Alta, sujeta a validación | Oportunidad en transición envío → pago |
| RN-04 | Proporcionar al usuario retroalimentación clara ante fallas de validación o procesamiento de pago | Media, sujeta a validación | Oportunidad en pago → compra |
| RN-05 | Validar las mejoras mediante pruebas controladas y métricas acordadas | Alta | No existe evidencia causal de los motivos de pérdida |

## 7. Requerimientos funcionales

| ID | Descripción verificable | Prioridad | Origen | Criterio de aceptación resumido |
|---|---|---|---|---|
| RF-01 | Registrar eventos de las etapas clave con nombre estándar, marca temporal y un identificador seudónimo conforme a política de privacidad | Alta | RN-01 | Las etapas críticas pueden reconstruirse en el entorno de prueba sin duplicaciones inesperadas |
| RF-02 | Generar un informe de conversión por etapas con definición de denominador, periodo y orden, señalando si mide usuarios o sesiones | Alta | RN-01 | El informe permite reproducir totales y tasas y muestra la metodología |
| RF-03 | Alertar sobre ausencias anómalas de eventos y fallos de instrumentación por día | Alta | RN-01 | Se identifica una interrupción de captura en una prueba controlada |
| RF-04 | Registrar tipos de error de formulario de envío mediante códigos no sensibles | Alta | RN-02 | El evento identifica campo/tipo de fallo sin contener dirección, correo, teléfono o tarjeta |
| RF-05 | Mostrar validaciones de envío en el campo correspondiente con mensajes comprensibles y accesibles | Media | RN-02 | Un valor inválido produce mensaje accionable y permite corregirlo sin borrar los demás datos válidos |
| RF-06 | Mostrar antes de confirmar la transición a pago un resumen de subtotal, envío, impuestos y total cuando correspondan | Alta | RN-03 | El total y sus componentes son visibles; si algún componente es estimado, se indica |
| RF-07 | Mostrar estado de procesamiento de pago, prevenir envíos múltiples desde la interfaz y presentar resultado comprensible | Media | RN-04 | Doble clic no genera dos solicitudes de compra desde la interfaz de prueba |
| RF-08 | Ofrecer, cuando el pago falla, una explicación no sensible y una vía para reintentar sin duplicar pedido | Media | RN-04 | El usuario puede reintentar con integridad de orden en pruebas de fallo simulado |
| RF-09 | Permitir comparar variantes de UX por cohortes experimentales, conservando asignación y eventos de resultado | Alta | RN-05 | Se obtiene reporte por variante con población y conversión comparables |
| RF-10 | Documentar y visualizar los pasos del checkout en formato BPMN AS-IS / TO-BE con decisiones y excepciones principales | Media | RN-02 a RN-04 | Diagrama revisable y trazable a RF-04–RF-08 |

**Convención:** requisitos RF-04 a RF-09 son propuestas para validar; no se ha demostrado que la tienda de muestra carezca de estas funcionalidades.

## 8. Requerimientos no funcionales

| ID | Requerimiento | Verificación propuesta |
|---|---|---|
| RNF-01 | Privacidad: no registrar PII ni datos completos de pago en eventos analíticos | Revisión de esquema y captura de eventos de prueba |
| RNF-02 | Accesibilidad: errores, estados y controles utilizables con teclado y tecnologías de asistencia, conforme a estándar definido por el proyecto (objetivo WCAG 2.2 AA) | Auditoría de accesibilidad y pruebas asistidas |
| RNF-03 | Integridad: un reintento no debe crear pedidos duplicados; la idempotencia debe garantizarse también en backend | Pruebas de reintentos y doble envío |
| RNF-04 | Trazabilidad: cambios a eventos y KPIs deben estar versionados | Revisión de documentación, SQL y control de versiones |
| RNF-05 | Rendimiento: la medición no debe degradar perceptiblemente el proceso de compra; fijar umbrales con Engineering antes del desarrollo | Línea base y pruebas de rendimiento acordadas |
| RNF-06 | Seguridad: las incidencias de pago no deben exponer información de proveedor, tokens ni detalles internos | Revisión de mensajes y logs de prueba |

## 9. Reglas de negocio

| ID | Regla |
|---|---|
| RB-01 | Las tasas de conversión deben indicar explícitamente numerador, denominador, ventana temporal y unidad de análisis |
| RB-02 | Las transiciones secuenciales se contabilizan solo si el evento posterior ocurre después del anterior dentro de la ventana establecida |
| RB-03 | El abandono se denominará **«no avance en la secuencia»** salvo que exista una definición adicional de abandono real con ventana de inactividad |
| RB-04 | No se mezclarán métricas de embudos con distinta población inicial, aunque compartan eventos |
| RB-05 | Ante errores de envío o pago, la aplicación debe informar al usuario sin revelar información sensible |
| RB-06 | No se declarará una mejora de conversión como efecto causal sin comparación experimental válida o evidencia equivalente |
| RB-07 | Toda intervención deberá permitir distinguir problema de experiencia de problema de instrumentación |

## 10. Métricas de éxito y línea base

| KPI | Definición | Línea base disponible | Uso |
|---|---|---|---|
| Conversión producto → carrito (secuencial) | Usuarios `add_to_cart` posteriores a `view_item` / usuarios `view_item` | 19,68 % | Diagnóstico; **no** meta de producción |
| Conversión completa del embudo principal | Usuarios que completan 4 etapas / usuarios `view_item` | 4,63 % | Diagnóstico; no tasa de compra por sesión |
| Conversión envío → pago (secuencial) | Usuarios `add_payment_info` posteriores a envío / usuarios que alcanzan envío en el subembudo | 65,79 % | Diagnóstico de transición |
| Conversión completa del subembudo | Usuarios con cuatro etapas checkout → compra / usuarios `begin_checkout` | 34,17 % | Diagnóstico; cohorte distinta del embudo principal |
| Cobertura de eventos | Días con presencia del evento / días analizados | `add_to_cart`: 74/92 días | Control inicial de instrumentación |
| Tasa de error de formulario | Interacciones con error / intentos de envío | No disponible | Requiere RF-04 |
| Tasa de error de pago | Intentos de pago con error / intentos de pago | No disponible | Requiere nueva instrumentación |

**Metas futuras:** deben acordarse con Product Owner tras validar instrumentación, construir una línea base en el sitio real y estimar tamaño muestral. No se fija arbitrariamente un porcentaje objetivo ni un incremento de ingresos.

## 11. Hipótesis para validación

| Hipótesis | Evidencia necesaria | Método sugerido |
|---|---|---|
| HYP-01: falta claridad o confianza en la ficha de producto | Pruebas de usabilidad y comportamiento por dispositivo | Investigación cualitativa y A/B test si aplica |
| HYP-02: el formulario de envío introduce fricción | Errores, tiempo de llenado, reintentos, sesiones | Telemetría no sensible y pruebas de tareas |
| HYP-03: la transición al pago genera dudas sobre costos | Encuestas, observación, comparativa de variantes | Prueba de claridad de costos y experimento |
| HYP-04: la instrumentación incompleta distorsiona el embudo | Auditoría de etiquetas y cobertura diaria | QA de tracking antes de intervenir UX |

## 12. Criterios de aceptación de negocio (alto nivel)

1. El equipo puede reproducir las métricas usando consultas versionadas y documentadas, y distinguir ambos embudos.
2. Un reporte indica claramente población, secuencia, unidad de análisis y limitaciones.
3. QA identifica un escenario con evento ausente y recibe una señal de anomalía de medición.
4. Los errores de envío se clasifican sin recolectar datos personales.
5. En un prototipo, los costos aplicables se muestran antes del pago y los errores pueden corregirse con mensajes accesibles.
6. Un pago simulado fallido y un doble clic no generan dos pedidos; el comportamiento backend debe confirmarse con prueba específica.
7. Un experimento propuesto incluye métrica primaria, condiciones de inclusión, duración/tamaño de muestra a calcular, criterios de parada y revisión de riesgos.

Estos criterios se descompondrán en escenarios Given/When/Then y casos UAT numerados.

## 13. Dependencias, riesgos y supuestos

| Tipo | Descripción | Mitigación |
|---|---|---|
| Dependencia | Acceso a eventos, definiciones analíticas y entorno de pruebas | Definir responsables de Analytics y QA |
| Riesgo | Eventos faltantes o inconsistentes | RF-03 y auditoría de instrumentación |
| Riesgo | Comparación de poblaciones incompatibles | RB-04; registrar definición y cohortes |
| Riesgo | Atribuir causalidad a cifras observacionales | Investigar y experimentar antes de concluir |
| Riesgo | Filtración de datos sensibles en eventos | RNF-01 y revisión de privacidad |
| Supuesto | El flujo de referencia contempla envío antes de pago | Validar con mapeo AS-IS y variantes reales |
| Supuesto | Existe capacidad técnica para cambios de UX | Estimar factibilidad con Engineering |

## 14. Priorización propuesta

**Primera fase — Medición y diagnóstico:** RF-01, RF-02, RF-03, RF-04 y RF-09; revisar hipótesis HYP-04 antes de atribuir pérdidas a UX.

**Segunda fase — Mejoras de experiencia sujetas a validación:** RF-05, RF-06, RF-07 y RF-08. Priorizar según investigación, impacto esperado, dependencia técnica y esfuerzo real.

**Documentación transversal:** RF-10; BPMN AS-IS/TO-BE, historias y UAT se vincularán a los RF correspondientes.

## 15. Matriz de trazabilidad inicial

| Necesidad | Requisitos | Evidencia / entregables posteriores |
|---|---|---|
| RN-01 Medición reproducible | RF-01, RF-02, RF-03 | SQL 01–03, CSV 01–03, UAT de instrumentación |
| RN-02 Comprender errores y fricción | RF-04, RF-05, RF-10 | BPMN AS-IS/TO-BE, historias HU-01/HU-02, UAT |
| RN-03 Transparencia de costos | RF-06, RF-10 | Historia HU-03, UAT de desglose de total |
| RN-04 Recuperación de errores de pago | RF-07, RF-08, RF-10 | Historia HU-04, UAT de doble envío/fallo |
| RN-05 Validar impacto | RF-09 | Diseño de experimento y reporte por variante |

*Los identificadores de historias son propuestos y se consolidarán al crear el entregable específico.*

## 16. Evidencias del repositorio

Rutas relativas a `caso_04_ecommerce_conversion/`:

- `sql/01_exploracion_eventos_ga4.sql` y `resultados/01_exploracion_eventos_ga4.csv`.
- `sql/02_funnel_conversion_ga4.sql` y `resultados/02_funnel_conversion_ga4.csv`.
- `sql/03_checkout_dropoff_ga4.sql` y `resultados/03_checkout_dropoff_ga4.csv`.
- `documentacion/04_analisis_hallazgos_comerciales.md`.
- **Este BRD:** `documentacion/BRD/05_brd_ecommerce_checkout.md`.

## 17. Próximas entregas y control de cambios

1. BPMN **AS-IS** (flujo observado/supuesto, con incertidumbres explícitas) y **TO-BE** (flujo propuesto).
2. Historias de usuario con criterios Given/When/Then por RF priorizado.
3. Matriz UAT trazada a historias y requisitos.
4. README del Caso 04 en español e inglés, evidencia visual y publicación en GitHub.

**Historial:** v1.0 — documento inicial basado en consultas 01, 02 y 03 y sus resultados compartidos. **Aprobaciones:** no aplica; ejercicio de portafolio.
