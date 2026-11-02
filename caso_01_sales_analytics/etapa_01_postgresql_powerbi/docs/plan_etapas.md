# Hoja de ruta y criterios de aceptación

## Etapa 1 — PostgreSQL + Power BI
- [ ] Confirmar esquema real y tipos.
- [ ] Revisar transformaciones y reglas sobre devoluciones, ventas, unidades, clientes y duplicados.
- [ ] Construir pruebas SQL con umbrales/estados PASS-FAIL.
- [ ] Conciliar indicadores SQL vs. DAX con filtros equivalentes.
- [ ] Publicar capturas de dashboard anonimizadas y diccionario de datos.

## Etapa 2 — BigQuery
- [ ] Definir dataset, región, permisos y presupuesto/cuotas.
- [ ] Exportar movimientos desidentificados y cargar a tabla staging.
- [ ] Escribir SQL compatible BigQuery y comparar conteos/sumas con PostgreSQL.
- [ ] Documentar idempotencia y controles de conciliación.

## Etapa 3 — Automatización
- [ ] Implementar extracción/carga mediante Python.
- [ ] Añadir ejecución programada (Cloud Run + Scheduler si se justifica).
- [ ] Añadir logs estructurados, reintentos, manejo de errores y prevención de duplicados.
- [ ] Probar fallos y reejecución segura.

## Etapa 4 — Claude API
- [ ] Generar tabla/vista de métricas agregadas y validadas.
- [ ] Construir cliente Claude por API usando secretos en variables de entorno.
- [ ] Exigir citas a métricas presentes y rechazar afirmaciones sin respaldo numérico.
- [ ] Pruebas deterministas de valores y límites de privacidad/costo.
