# Etapa 2 — carga y conciliación inicial (V11)

## Entorno confirmado
- Proyecto: `retail-data-engineering-512100`.
- Dataset: `retail_analytics` (región `us-central1`).
- BigQuery Sandbox, sin facturación configurada en el momento de la creación.
- Origen PostgreSQL: base `portafolio_retail`, tabla `public.base_movimientos`.

## Datos y alcance
Archivo local de carga: `movimientos_retail_bigquery_v02.csv`, con **1.033.036 filas de datos** y cabecera (1.033.037 líneas verificadas en Excel). Se exportaron únicamente 13 columnas comerciales: `id_linea`, `factura`, `producto`, `cantidad`, `fecha`, `precio_gbp`, `importe_gbp`, `clase_codigo`, `tipo_movimiento`, `incluir_ventas_brutas`, `incluir_abonos_mercancia`, `incluir_recompra` e `incluir_demanda_unidades`. Se excluyó `cliente_id`, por lo que no se reproduce analítica de clientes en BigQuery en esta entrega. **No incluir el CSV en GitHub**.

## Resultados ejecutados y observados
| Métrica | PostgreSQL | BigQuery |
|---|---:|---:|
| Movimientos | 1.033.036 | 1.033.036 |
| Ventas brutas GBP | 19.643.861,637 | 19.643.861,637 |
| Abonos GBP | -716.462,57 | -716.462,57 |
| Ventas netas GBP | 18.927.399,067 | 18.927.399,067 |
| Unidades elegibles | 11.188.061 | 11.188.061 |
| Facturas venta | 39.516 | 39.516 |
| Combinaciones producto-mes | No verificado aquí | 67.205 |

Conciliación producto-mes: mismas unidades e importes que en vista resumen, según resultado compartido. Diferencia en estas métricas: 0. `vw_producto_mes` se creó mediante `CREATE OR REPLACE VIEW` y se consultó correctamente.

## Orden de ejecución
1. Cargar CSV como tabla `movimientos_raw` con esquema manual, cabecera omitida (1), formato CSV.
2. Ejecutar `sql/01_conciliacion_carga.sql`.
3. Ejecutar `sql/02_vw_resumen_comercial.sql`.
4. Ejecutar `sql/03_vw_producto_mes.sql`.
5. Ejecutar `sql/04_conciliacion_producto_mes.sql`.

## Estado pendiente para cerrar etapa 2
- Implementar extracción/carga reproducible con Python o cliente SQL y estrategia de sustitución de datos (evitar anexos duplicados).
- Versionar esquema de tabla y procedimiento de carga (sin secretos).
- Definir prueba automatizable de conciliación y manejo de errores, antes de la etapa 3.
