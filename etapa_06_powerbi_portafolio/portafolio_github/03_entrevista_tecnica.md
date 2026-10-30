# Cómo presentar el proyecto en entrevista

**Resumen de 45 segundos:** Implementé un flujo de análisis comercial que consolida datos transaccionales en PostgreSQL, replica los movimientos a BigQuery mediante un pipeline Python compatible con Sandbox y transforma indicadores agregados en alertas explicables. Desarrollé un motor de reglas que identifica concentración ABC y tasas de abonos elevadas, cuidando calidad, granularidad, rastreabilidad y límites de los datos históricos. Presento los resultados en Power BI, con informes CSV/JSON y documentación técnica reproducible.

**Arquitectura y transferencia de habilidades:** SQL + DAX + Power BI + Python/ETL + GCP BigQuery + observabilidad (log, bloqueo concurrente, historial). Claude API es un conector optativo, **no está integrado en producción ni se ha probado con uso pagado**.

**Tres decisiones técnicas defendibles:**
- Copy job / WRITE_TRUNCATE reemplaza MERGE por restricciones de BigQuery Sandbox.
- ABC se calcula por código de producto consolidado sobre base positiva; no se confunde con total neto global.
- Las alertas son reglas deterministas y auditables, no causalidad ni predicción.

**Qué no afirmar:** No atribuir experiencias laborales de Data Engineer basadas solamente en el proyecto; no asegurar automatización en nube 24/7 (scheduler corre en un PC); no decir que Claude generó las reglas; no presentar ventas de 2009–2011 como actuales.
