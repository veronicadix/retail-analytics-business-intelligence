# Arquitectura y decisiones técnicas

1. **PostgreSQL** (`portafolio_retail`): ingesta preexistente, controles de calidad y vistas; catálogo de productos y Pareto por código único.
2. **Python / extracción**: lectura de movimientos, staging en BigQuery, validación de conteos y reemplazo de raw mediante *copy job* compatible con Sandbox.
3. **BigQuery** (`retail-data-engineering-512100.retail_analytics`): agregaciones de indicadores y ventas por producto. El proyecto cloud aquí nombrado corresponde al entorno de demostración, no supone acceso público.
4. **Motor Python de informes**: une agregados de BigQuery con descripciones y ABC desde PostgreSQL; consolida filas repetidas por código.
5. **Reglas deterministas**: hallazgos con evidencia, acción sugerida y límites de interpretación; salidas Markdown/JSON/CSV locales.
6. **Power BI**: página de inteligencia comercial basada en exportaciones, con KPI, ABC, Top 10, alertas y trazabilidad.

**Automatización:** una tarea semanal los lunes 08:00, configurada con el Programador de tareas de Windows; requiere equipo encendido, sesión de usuario y conectividad. No afirmar operación 24/7.

**Separación de fuentes:** el Top 10 financiero proviene de BigQuery; descripción y Pareto se obtienen de PostgreSQL. El contenido compartido no incluye datos a nivel de cliente.

**Reproducibilidad parcial:** para reproducir el proceso completo se necesitan datos originales, PostgreSQL y acceso configurado a BigQuery; no se incluyen aquí datos privados ni credenciales.
