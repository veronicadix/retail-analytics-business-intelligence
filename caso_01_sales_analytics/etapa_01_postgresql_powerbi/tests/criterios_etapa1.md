# Pruebas de aceptación — Etapa 1

1. El inventario encuentra las tres tablas esperadas y sus columnas utilizadas.
2. Las consultas se ejecutan en PostgreSQL sin alterar datos.
3. Ventas brutas, abonos y netas se concilian con Power BI para idénticos filtros y fecha de corte.
4. No hay clasificación doble inesperada para flags de ventas/abonos; si la hay, se justifica por una regla documentada.
5. Los nulos en métricas/flags críticos quedan cuantificados y tratados explícitamente.
6. Todos los cambios de SQL, reglas y resultados están versionados sin datos personales.
