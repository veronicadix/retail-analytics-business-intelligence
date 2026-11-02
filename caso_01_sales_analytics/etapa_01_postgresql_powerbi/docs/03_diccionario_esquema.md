# Etapa 1 — Diccionario de esquema (paso 3)

**Base:** `portafolio_retail` · **Esquema:** `public` · **Fecha:** 2026-10-16

Datos obtenidos de `03_resumen_columnas.sql`. `YES` indica que se permiten nulos, no que se hayan encontrado.

## `public.base_movimientos` — 19 columnas

| Pos. | Campo | Tipo | Admite NULL |
|---:|---|---|---|
| 1 | `id_linea` | text | NO |
| 2 | `hoja_origen` | text | YES |
| 3 | `fila_excel` | integer | YES |
| 4 | `factura` | text | YES |
| 5 | `producto` | text | YES |
| 6 | `descripcion` | text | YES |
| 7 | `cantidad` | numeric | YES |
| 8 | `fecha` | timestamp without time zone | YES |
| 9 | `precio_gbp` | numeric | YES |
| 10 | `cliente_id` | text | YES |
| 11 | `pais` | text | YES |
| 12 | `importe_gbp` | numeric | YES |
| 13 | `clase_codigo` | text | YES |
| 14 | `tipo_movimiento` | text | YES |
| 15 | `incluir_ventas_brutas` | smallint | YES |
| 16 | `incluir_abonos_mercancia` | smallint | YES |
| 17 | `incluir_recompra` | smallint | YES |
| 18 | `incluir_demanda_unidades` | smallint | YES |
| 19 | `motivo_alcance` | text | YES |

## `public.catalogo_codigos` — 7 columnas

| Pos. | Campo | Tipo | Admite NULL |
|---:|---|---|---|
| 1 | `producto` | text | NO |
| 2 | `clase_codigo` | text | YES |
| 3 | `descripcion_referencia` | text | YES |
| 4 | `variantes_descripcion_en_ventas` | integer | YES |
| 5 | `filas_conservadas` | integer | YES |
| 6 | `lineas_venta` | integer | YES |
| 7 | `regla_origen` | text | YES |

## `public.facturas_venta` — 10 columnas

| Pos. | Campo | Tipo | Admite NULL |
|---:|---|---|---|
| 1 | `factura` | text | NO |
| 2 | `cliente_id` | text | YES |
| 3 | `pais` | text | YES |
| 4 | `fecha_factura` | timestamp without time zone | YES |
| 5 | `ultima_fecha_linea` | timestamp without time zone | YES |
| 6 | `flag_varias_horas` | smallint | YES |
| 7 | `lineas_mercancia` | integer | YES |
| 8 | `unidades_mercancia` | numeric | YES |
| 9 | `importe_bruto_mercancia_gbp` | numeric | YES |
| 10 | `incluir_recompra` | smallint | YES |

## Vistas existentes

`vw_indicadores_producto`, `vw_perfil_clientes`, `vw_producto_mes`, `vw_recompra_producto`, `vw_segmentos_clientes`, `vw_valor_clientes`. **Sus definiciones no se han auditado aún.**
