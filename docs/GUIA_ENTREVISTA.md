# Guion de presentación (45–60 segundos)

«Desarrollé un proyecto de ingeniería de datos y BI para priorización comercial. Preparé información histórica de ventas en PostgreSQL, la llevé a BigQuery Sandbox con Python y conciliaciones, y construí un motor de reglas para emitir alertas trazables con recomendaciones y limitaciones. Presenté indicadores ABC, devoluciones y un ranking Top 10 en Power BI. La automatización usa Windows Task Scheduler en un PC local; los componentes de IA generativa permanecen opcionales y no intervienen en los resultados de reglas».

## Decisiones que conviene explicar

- **Sandbox:** sustitución de `MERGE` por staging y BigQuery copy job con reemplazo de tabla.
- **Granularidad:** consolidación por código antes de categorizar ABC, preservando trazabilidad de 170 filas adicionales.
- **Métrica:** base positiva de Pareto distinta del neto global por GBP 564,26.
- **Observabilidad:** logs, historial JSONL y bloqueo por archivo local; no equivale a una infraestructura administrada en la nube.
- **Acción comercial:** las alertas señalan revisiones, no causas demostradas.
