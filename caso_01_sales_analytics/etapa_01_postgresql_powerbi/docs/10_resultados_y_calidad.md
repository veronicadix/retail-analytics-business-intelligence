# V10 — Resultados confirmados en ejecución

**Conexión:** PostgreSQL `localhost:5432`, base **`portafolio_retail`**, usuario local `postgres` (no se almacena contraseña).

## Inventario base
- 3 tablas: `base_movimientos` (1.033.036), `catalogo_codigos` (5.304), `facturas_venta` (39.516).
- 6 vistas iniciales: `vw_indicadores_producto`, `vw_perfil_clientes`, `vw_producto_mes`, `vw_recompra_producto`, `vw_segmentos_clientes`, `vw_valor_clientes`.
- 2 vistas creadas posteriormente: `vw_resumen_comercial`, `vw_pareto_productos`.

## Conciliación comercial
| Métrica | GBP |
|---|---:|
| Ventas brutas mercancía | 19.643.861,637 |
| Abonos mercancía | -716.462,570 |
| Ventas netas mercancía | 18.927.399,067 |
| Diferencia de conciliación | 0,000 |

Otros: 11.188.061 unidades, 39.516 facturas, 5.852 clientes identificados, fecha mínima 2009-12-01 07:45 y máxima 2011-12-09 12:50.

## Calidad verificada
- 21 verificaciones iniciales reportadas sin incidencias, entre ellas identificación nula/duplicada, fechas/importe/cantidad nulos y flags fuera de 0/1.
- 5 verificaciones posteriores de coherencia de flags: todas con resultado 0.
- Matriz de alcance de todos los movimientos: total monetario **18.855.533,70 GBP**, **no equivale** a ventas netas de mercancía por incluir clases no comerciales.

## Pareto/ABC (sobre productos con venta neta positiva)
| Categoría | Productos | GBP |
|---|---:|---:|
| A | 1.049 | 15.145.991,87 |
| B | 1.276 | 2.836.580,94 |
| C | 2.550 | 945.390,52 |
| Total | 4.875 | 18.927.963,33 |

La diferencia de 564,263 GBP frente a las ventas netas de mercancía se debe al alcance positivo del Pareto. No mezclar denominadores.

## Clientes y comparación de años
- Clientes analizados: 5.852. Clientes con 2 o más compras: 4.234. Ticket promedio: 466,43 GBP.
- Segmentos: Reactivar selectivamente 2.619; Desarrollar clientes activos 1.731; Fidelizar alto valor 1.183; Reactivar alto valor 266; Revisar abonos 41; Desarrollar alto valor 12.
- Variación anual observada: -1,34 % (incluye diciembre parcial 2011); enero–noviembre comparable: +0,02 % (resultado de la tarjeta).
