# Caso 04 — Entregable 08: Matriz de pruebas UAT

**Proyecto:** Retail Analytics & Business Intelligence — E-commerce Conversion & Business Requirements  
**Versión:** 1.0 — diseño de pruebas; no ejecutadas  
**Estado:** 31 escenarios propuestos; 0 aprobados, 0 fallidos, 31 no ejecutados.  
**Fuentes:** `05_brd_ecommerce_checkout.md`, `07_historias_usuario_criterios_aceptacion.md`, BPMN AS-IS/TO-BE, SQL 01–03.

## 1. Objetivo y alcance

Verificar criterios de aceptación de HU-01 a HU-10 mediante escenarios de aceptación para instrumentación GA4, reportes, alertas, envío, costos, pagos, experimentos y modelado BPMN. El dataset GA4 histórico sustenta el diagnóstico, pero **no sustituye un entorno transaccional de pruebas** ni demuestra que funcionalidades propuestas estén implementadas.

## 2. Evidencia de referencia (no resultado de UAT)

| Fuente | Referencia | Alcance |
|---|---:|---|
| Embudo principal | 61.252 → 12.052 → 4.909 → 2.833 | Secuencia por usuario de producto a compra, 4,63 % |
| Checkout independiente | 9.715 → 6.588 → 4.334 → 3.320 | Secuencia de checkout a compra, 34,17 % |
| Cobertura de `add_to_cart` | 74 de 92 días | Señal para revisión de instrumentación, no fallo verificado |

**No mezclar:** los embudos tienen universos de partida diferentes. Las tasas de no avance no prueban abandono causal.

## 3. Reglas de ejecución

- Estados permitidos: **No ejecutado**, **Bloqueado**, **Aprobado**, **Fallido**, **No aplica**.
- Registrar resultado obtenido, fecha, ejecutor, evidencia verificable y defecto si aplica. No marcar **Aprobado** sin evidencia real.
- Para pruebas de pagos utilizar exclusivamente sandbox, datos de prueba y contratos autorizados; no usar tarjetas ni datos personales reales.
- Validar condiciones de consentimiento, políticas de privacidad, permisos y accesibilidad antes de iniciar.
- Las métricas históricas pueden reproducirse desde SQL; las funciones nuevas requieren una aplicación o prototipo implementado.
- UAT debe revisarse con Product Owner y QA; la presente matriz es una propuesta académica/profesional de portafolio.

## 4. Resumen de cobertura

| Historia | Requisito | Casos UAT | Prioridad | Estado |
|---|---|---:|---|---|
| HU-01 — Instrumentación estándar de eventos | RF-01 | 3 | P0 | No ejecutado |
| HU-02 — Informe reproducible de conversión | RF-02 | 4 | P0 | No ejecutado |
| HU-03 — Alerta de cobertura e instrumentación | RF-03 | 3 | P0 | No ejecutado |
| HU-04 — Telemetría no sensible de errores de envío | RF-04 | 3 | P1 | No ejecutado |
| HU-05 — Validación accesible del formulario de envío | RF-05 | 3 | P2 | No ejecutado |
| HU-06 — Desglose transparente del costo antes del pago | RF-06 | 3 | P2 | No ejecutado |
| HU-07 — Estado de pago y prevención de doble envío | RF-07 | 3 | P2 | No ejecutado |
| HU-08 — Recuperación de fallas de pago | RF-08 | 3 | P2 | No ejecutado |
| HU-09 — Evaluación controlada de cambios de UX | RF-09 | 3 | P1 | No ejecutado |
| HU-10 — Documentación BPMN trazable | RF-10 | 3 | P1 | No ejecutado |

**Cobertura de diseño:** 31 de 31 criterios de aceptación tienen un caso UAT (100 % de trazabilidad documental). **Cobertura de ejecución:** 0 de 31 (0 %).

## 5. Casos de prueba detallados

### UAT-001 — HU-01 · CA-HU01-01

**Escenario:** Instrumentación estándar de eventos  
**Trazabilidad:** RF-01 / HU-01 / CA-HU01-01 · **Prioridad:** P0 · **Tipo:** Datos / Seguridad  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un entorno de prueba con consentimiento válido según la política aplicable  
**Pasos:**
1. Preparar el escenario: un entorno de prueba con consentimiento válido según la política aplicable.
2. Ejecutar: se ejecutan las acciones de producto, carrito, checkout, envío, pago y compra.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Cada acción instrumentada genera el evento esperado con nombre, timestamp y seudónimo permitido.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-002 — HU-01 · CA-HU01-02

**Escenario:** Instrumentación estándar de eventos  
**Trazabilidad:** RF-01 / HU-01 / CA-HU01-02 · **Prioridad:** P0 · **Tipo:** Datos / Seguridad  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un evento capturado  
**Pasos:**
1. Preparar el escenario: un evento capturado.
2. Ejecutar: QA inspecciona su payload.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** No contiene dirección, correo, teléfono, número de tarjeta ni información personal prohibida.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-003 — HU-01 · CA-HU01-03

**Escenario:** Instrumentación estándar de eventos  
**Trazabilidad:** RF-01 / HU-01 / CA-HU01-03 · **Prioridad:** P0 · **Tipo:** Datos / Seguridad  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un flujo de prueba de una sola acción  
**Pasos:**
1. Preparar el escenario: un flujo de prueba de una sola acción.
2. Ejecutar: se inspeccionan los registros.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** No existen duplicaciones inesperadas del mismo evento; los reintentos legítimos quedan diferenciados según diseño acordado.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-004 — HU-02 · CA-HU02-01

**Escenario:** Informe reproducible de conversión  
**Trazabilidad:** RF-02 / HU-02 / CA-HU02-01 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** BigQuery + snapshot de referencia  
**Precondición:** un periodo y un embudo definidos  
**Pasos:**
1. Preparar el escenario: un periodo y un embudo definidos.
2. Ejecutar: ejecuto el reporte.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Aparecen conteos por etapa, conversión entre etapas y acumulada, fórmula, unidad de análisis, ventana temporal y versión de consulta.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-005 — HU-02 · CA-HU02-02

**Escenario:** Informe reproducible de conversión  
**Trazabilidad:** RF-02 / HU-02 / CA-HU02-02 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** BigQuery + snapshot de referencia  
**Precondición:** las consultas de referencia 02 y 03  
**Pasos:**
1. Preparar el escenario: las consultas de referencia 02 y 03.
2. Ejecutar: reproduzco las métricas sobre el mismo snapshot y las mismas reglas.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Obtengo los conteos documentados o registro explícitamente la diferencia y su causa.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-006 — HU-02 · CA-HU02-03

**Escenario:** Informe reproducible de conversión  
**Trazabilidad:** RF-02 / HU-02 / CA-HU02-03 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** BigQuery + snapshot de referencia  
**Precondición:** dos embudos con poblaciones iniciales distintas  
**Pasos:**
1. Preparar el escenario: dos embudos con poblaciones iniciales distintas.
2. Ejecutar: visualizo ambos reportes.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se muestra una advertencia de no comparabilidad directa.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-007 — HU-02 · CA-HU02-04

**Escenario:** Informe reproducible de conversión  
**Trazabilidad:** RF-02 / HU-02 / CA-HU02-04 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** BigQuery + snapshot de referencia  
**Precondición:** un evento posterior con timestamp igual o anterior al evento anterior  
**Pasos:**
1. Preparar el escenario: un evento posterior con timestamp igual o anterior al evento anterior.
2. Ejecutar: calculo el embudo.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** No cuenta como avance secuencial conforme a la regla acordada.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-008 — HU-03 · CA-HU03-01

**Escenario:** Alerta de cobertura e instrumentación  
**Trazabilidad:** RF-03 / HU-03 / CA-HU03-01 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un día de prueba con ausencia artificial de un evento crítico  
**Pasos:**
1. Preparar el escenario: un día de prueba con ausencia artificial de un evento crítico.
2. Ejecutar: se ejecuta el control.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se emite una alerta con evento, fecha, condición y evidencia.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-009 — HU-03 · CA-HU03-02

**Escenario:** Alerta de cobertura e instrumentación  
**Trazabilidad:** RF-03 / HU-03 / CA-HU03-02 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un día sin actividad esperada validado por negocio  
**Pasos:**
1. Preparar el escenario: un día sin actividad esperada validado por negocio.
2. Ejecutar: se ejecuta el control.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** No se clasifica automáticamente como incidencia sin considerar calendario y umbrales acordados.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-010 — HU-03 · CA-HU03-03

**Escenario:** Alerta de cobertura e instrumentación  
**Trazabilidad:** RF-03 / HU-03 / CA-HU03-03 · **Prioridad:** P0 · **Tipo:** Analytics / SQL  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un hallazgo de cobertura  
**Pasos:**
1. Preparar el escenario: un hallazgo de cobertura.
2. Ejecutar: se revisa el reporte.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se puede registrar estado, responsable y resolución.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-011 — HU-04 · CA-HU04-01

**Escenario:** Telemetría no sensible de errores de envío  
**Trazabilidad:** RF-04 / HU-04 / CA-HU04-01 · **Prioridad:** P1 · **Tipo:** Datos / Seguridad  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un dato de prueba inválido  
**Pasos:**
1. Preparar el escenario: un dato de prueba inválido.
2. Ejecutar: falla la validación de envío.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se registra un código de error y tipo de campo previamente aprobados, sin el valor ingresado.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-012 — HU-04 · CA-HU04-02

**Escenario:** Telemetría no sensible de errores de envío  
**Trazabilidad:** RF-04 / HU-04 / CA-HU04-02 · **Prioridad:** P1 · **Tipo:** Datos / Seguridad  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un evento de error  
**Pasos:**
1. Preparar el escenario: un evento de error.
2. Ejecutar: se inspecciona su contenido.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** No incluye PII ni datos de pago.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-013 — HU-04 · CA-HU04-03

**Escenario:** Telemetría no sensible de errores de envío  
**Trazabilidad:** RF-04 / HU-04 / CA-HU04-03 · **Prioridad:** P1 · **Tipo:** Datos / Seguridad  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un conjunto de errores de prueba  
**Pasos:**
1. Preparar el escenario: un conjunto de errores de prueba.
2. Ejecutar: se genera el reporte.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Los errores pueden agruparse por tipo y periodo sin exponer información sensible.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-014 — HU-05 · CA-HU05-01

**Escenario:** Validación accesible del formulario de envío  
**Trazabilidad:** RF-05 / HU-05 / CA-HU05-01 · **Prioridad:** P2 · **Tipo:** Funcional / UX  
**Ambiente:** Aplicación QA / datos sintéticos  
**Precondición:** un campo obligatorio vacío  
**Pasos:**
1. Preparar el escenario: un campo obligatorio vacío.
2. Ejecutar: intento continuar.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Veo un mensaje específico junto al campo y el foco se gestiona de modo accesible.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-015 — HU-05 · CA-HU05-02

**Escenario:** Validación accesible del formulario de envío  
**Trazabilidad:** RF-05 / HU-05 / CA-HU05-02 · **Prioridad:** P2 · **Tipo:** Funcional / UX  
**Ambiente:** Aplicación QA / datos sintéticos  
**Precondición:** un campo inválido y otros correctos  
**Pasos:**
1. Preparar el escenario: un campo inválido y otros correctos.
2. Ejecutar: corrijo el error.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Los demás datos válidos se conservan.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-016 — HU-05 · CA-HU05-03

**Escenario:** Validación accesible del formulario de envío  
**Trazabilidad:** RF-05 / HU-05 / CA-HU05-03 · **Prioridad:** P2 · **Tipo:** Funcional / UX  
**Ambiente:** Aplicación QA / datos sintéticos  
**Precondición:** un usuario que navega solo con teclado o lector de pantalla  
**Pasos:**
1. Preparar el escenario: un usuario que navega solo con teclado o lector de pantalla.
2. Ejecutar: ocurre un error.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** El mensaje puede percibirse y asociarse al campo afectado según el estándar de accesibilidad aprobado (objetivo WCAG 2.2 AA).

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-017 — HU-06 · CA-HU06-01

**Escenario:** Desglose transparente del costo antes del pago  
**Trazabilidad:** RF-06 / HU-06 / CA-HU06-01 · **Prioridad:** P2 · **Tipo:** Funcional / UX  
**Ambiente:** Aplicación QA / datos sintéticos  
**Precondición:** un carrito con envío e impuestos aplicables  
**Pasos:**
1. Preparar el escenario: un carrito con envío e impuestos aplicables.
2. Ejecutar: avanzo hacia pago.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** El resumen muestra cada componente y el total de forma consistente.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-018 — HU-06 · CA-HU06-02

**Escenario:** Desglose transparente del costo antes del pago  
**Trazabilidad:** RF-06 / HU-06 / CA-HU06-02 · **Prioridad:** P2 · **Tipo:** Funcional / UX  
**Ambiente:** Aplicación QA / datos sintéticos  
**Precondición:** un componente pendiente de cálculo  
**Pasos:**
1. Preparar el escenario: un componente pendiente de cálculo.
2. Ejecutar: veo el resumen.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se identifica claramente como estimado y no como importe definitivo.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-019 — HU-06 · CA-HU06-03

**Escenario:** Desglose transparente del costo antes del pago  
**Trazabilidad:** RF-06 / HU-06 / CA-HU06-03 · **Prioridad:** P2 · **Tipo:** Funcional / UX  
**Ambiente:** Aplicación QA / datos sintéticos  
**Precondición:** un cambio de dirección o modalidad de envío  
**Pasos:**
1. Preparar el escenario: un cambio de dirección o modalidad de envío.
2. Ejecutar: se recalculan costos.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** El total visible se actualiza antes de confirmar la compra.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-020 — HU-07 · CA-HU07-01

**Escenario:** Estado de pago y prevención de doble envío  
**Trazabilidad:** RF-07 / HU-07 / CA-HU07-01 · **Prioridad:** P2 · **Tipo:** Integración / pagos  
**Ambiente:** Aplicación QA / sandbox de pagos  
**Precondición:** un pago en procesamiento  
**Pasos:**
1. Preparar el escenario: un pago en procesamiento.
2. Ejecutar: pulso de nuevo el botón de confirmar.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** La interfaz no dispara una segunda solicitud de creación de pedido.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-021 — HU-07 · CA-HU07-02

**Escenario:** Estado de pago y prevención de doble envío  
**Trazabilidad:** RF-07 / HU-07 / CA-HU07-02 · **Prioridad:** P2 · **Tipo:** Integración / pagos  
**Ambiente:** Aplicación QA / sandbox de pagos  
**Precondición:** un procesamiento terminado  
**Pasos:**
1. Preparar el escenario: un procesamiento terminado.
2. Ejecutar: se recibe éxito o fallo.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** El usuario ve un estado comprensible sin información interna del proveedor de pago.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-022 — HU-07 · CA-HU07-03

**Escenario:** Estado de pago y prevención de doble envío  
**Trazabilidad:** RF-07 / HU-07 / CA-HU07-03 · **Prioridad:** P2 · **Tipo:** Integración / pagos  
**Ambiente:** Aplicación QA / sandbox de pagos  
**Precondición:** la repetición del mismo identificador de operación en backend  
**Pasos:**
1. Preparar el escenario: la repetición del mismo identificador de operación en backend.
2. Ejecutar: se reciben solicitudes duplicadas.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se conserva una única orden conforme al contrato de idempotencia acordado.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-023 — HU-08 · CA-HU08-01

**Escenario:** Recuperación de fallas de pago  
**Trazabilidad:** RF-08 / HU-08 / CA-HU08-01 · **Prioridad:** P2 · **Tipo:** Integración / pagos  
**Ambiente:** Aplicación QA / sandbox de pagos  
**Precondición:** un pago fallido simulado  
**Pasos:**
1. Preparar el escenario: un pago fallido simulado.
2. Ejecutar: la respuesta llega a la interfaz.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se presenta un mensaje no sensible y una acción de reintento cuando corresponde.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-024 — HU-08 · CA-HU08-02

**Escenario:** Recuperación de fallas de pago  
**Trazabilidad:** RF-08 / HU-08 / CA-HU08-02 · **Prioridad:** P2 · **Tipo:** Integración / pagos  
**Ambiente:** Aplicación QA / sandbox de pagos  
**Precondición:** un reintento autorizado  
**Pasos:**
1. Preparar el escenario: un reintento autorizado.
2. Ejecutar: el comprador vuelve a pagar.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** El pedido conserva su integridad y no aparecen dos órdenes por la misma operación.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-025 — HU-08 · CA-HU08-03

**Escenario:** Recuperación de fallas de pago  
**Trazabilidad:** RF-08 / HU-08 / CA-HU08-03 · **Prioridad:** P2 · **Tipo:** Integración / pagos  
**Ambiente:** Aplicación QA / sandbox de pagos  
**Precondición:** un resultado incierto o timeout  
**Pasos:**
1. Preparar el escenario: un resultado incierto o timeout.
2. Ejecutar: el usuario consulta su estado.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** El sistema no afirma que el pago falló o tuvo éxito sin confirmación confiable.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-026 — HU-09 · CA-HU09-01

**Escenario:** Evaluación controlada de cambios de UX  
**Trazabilidad:** RF-09 / HU-09 / CA-HU09-01 · **Prioridad:** P1 · **Tipo:** Analytics / SQL  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** dos variantes de prueba  
**Pasos:**
1. Preparar el escenario: dos variantes de prueba.
2. Ejecutar: un usuario elegible entra en el experimento.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se registra asignación consistente, exposición y eventos de resultado conforme a la política de privacidad.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-027 — HU-09 · CA-HU09-02

**Escenario:** Evaluación controlada de cambios de UX  
**Trazabilidad:** RF-09 / HU-09 / CA-HU09-02 · **Prioridad:** P1 · **Tipo:** Analytics / SQL  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un reporte experimental  
**Pasos:**
1. Preparar el escenario: un reporte experimental.
2. Ejecutar: se revisan resultados.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se muestran población elegible, exclusiones, métricas primarias, intervalos de incertidumbre y problemas de instrumentación conocidos.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-028 — HU-09 · CA-HU09-03

**Escenario:** Evaluación controlada de cambios de UX  
**Trazabilidad:** RF-09 / HU-09 / CA-HU09-03 · **Prioridad:** P1 · **Tipo:** Analytics / SQL  
**Ambiente:** Entorno instrumentado QA / datos sintéticos  
**Precondición:** un experimento propuesto  
**Pasos:**
1. Preparar el escenario: un experimento propuesto.
2. Ejecutar: se solicita aprobación.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Existe protocolo con hipótesis, tamaño muestral a calcular, criterios de parada y monitoreo de riesgos antes de lanzarlo.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-029 — HU-10 · CA-HU10-01

**Escenario:** Documentación BPMN trazable  
**Trazabilidad:** RF-10 / HU-10 / CA-HU10-01 · **Prioridad:** P1 · **Tipo:** Documentación / revisión  
**Ambiente:** Editor BPMN + repositorio local  
**Precondición:** el archivo AS-IS  
**Pasos:**
1. Preparar el escenario: el archivo AS-IS.
2. Ejecutar: el equipo lo revisa.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Queda explícito que es una reconstrucción conceptual basada en eventos GA4, no una observación completa de la operación real.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-030 — HU-10 · CA-HU10-02

**Escenario:** Documentación BPMN trazable  
**Trazabilidad:** RF-10 / HU-10 / CA-HU10-02 · **Prioridad:** P1 · **Tipo:** Documentación / revisión  
**Ambiente:** Editor BPMN + repositorio local  
**Precondición:** el TO-BE  
**Pasos:**
1. Preparar el escenario: el TO-BE.
2. Ejecutar: QA revisa los caminos principales.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Se identifican validación de envío, visualización de total, confirmación de pago y manejo de errores/reintentos.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

### UAT-031 — HU-10 · CA-HU10-03

**Escenario:** Documentación BPMN trazable  
**Trazabilidad:** RF-10 / HU-10 / CA-HU10-03 · **Prioridad:** P1 · **Tipo:** Documentación / revisión  
**Ambiente:** Editor BPMN + repositorio local  
**Precondición:** un requerimiento RF-04 a RF-08  
**Pasos:**
1. Preparar el escenario: un requerimiento RF-04 a RF-08.
2. Ejecutar: se revisa la trazabilidad.
3. Capturar evidencia de la ejecución y revisar el resultado observable.
**Resultado esperado:** Puede vincularse a una actividad o decisión del TO-BE y al menos un criterio de aceptación de este backlog.

**Resultado real:** Pendiente · **Estado:** No ejecutado · **Evidencia:** Pendiente · **Defecto:** —

## 6. Registro de incidencias y decisión de aceptación

Al ejecutar los casos, registrar para cada fallo: ID de defecto, severidad (Crítica/Alta/Media/Baja), pasos de reproducción, esperado vs. real, captura o log redactado y responsable. Los defectos críticos o altos deben resolverse o recibir una excepción formal antes de la aceptación.

**Criterio propuesto de cierre UAT:** 100 % de casos aplicables ejecutados; cero defectos críticos/altos abiertos; excepciones documentadas y aprobadas por Product Owner; pruebas de privacidad y de integridad de pago satisfactorias. Esto requiere aprobación, no es un compromiso ya acordado.

## 7. Archivo operativo

Utilizar `08_matriz_pruebas_uat.csv` como matriz editable en Excel/Sheets. Filtrar por historia, prioridad, estado y requisito. Conservar este Markdown como documentación versionada.

## 8. Próximos pasos

1. Revisar criterios con Product Owner y QA; acordar umbrales, contratos y datos de prueba.
2. Ejecutar UAT solo cuando exista implementación o ambiente de prueba.
3. Registrar evidencias y defectos sin alterar los resultados históricos GA4.
4. Publicar ambos archivos y enlazarlos desde el README del Caso 04.
