# Etapa 1 — V05: Conciliación comercial

Fecha: 2026-10-16
Base: `portafolio_retail` | Tabla: `public.base_movimientos`

## Evidencia aportada (PostgreSQL)

| Métrica | GBP, sin redondear |
|---|---:|
| Ventas brutas (flag `incluir_ventas_brutas = 1`) | 19643861.637 |
| Abonos de mercancía (flag `incluir_abonos_mercancia = 1`) | -716462.57 |
| Ventas netas (ambos flags mediante OR) | 18927399.067 |

## Resultado

La suma de ventas brutas y abonos es 18927399.067 GBP, que coincide con el total informado como ventas netas. La conciliación de agregados pasa con diferencia cero. **Pendiente:** comprobar que los dos flags no se activen a la vez en ninguna fila y que los importes coincidan con la clasificación de las líneas. La igualdad de agregados no prueba estas condiciones.

## Evidencia previa conservada

- 3 tablas, 6 vistas en esquema `public`.
- Filas: `base_movimientos` 1033036; `catalogo_codigos` 5304; `facturas_venta` 39516.
- Columnas: 19, 7 y 10 respectivamente.
- 21 controles informados con valor de incidencia cero (nulos, duplicados e indicadores fuera de 0/1).
- Rango de `fecha`: 2009-12-01 07:45:00 a 2011-12-09 12:50:00.

## Paso siguiente

Ejecutar `sql/03_validaciones/05_coherencia_flags.sql`, guardar el resultado y definir la aceptación antes de avanzar al control de facturas / Power BI.
