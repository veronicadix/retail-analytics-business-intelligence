# V09 — Resultado de la vista comercial y transición a Power BI

**Fecha:** 2026-10-16  
**Base de datos:** `portafolio_retail`  
**Objeto:** `public.vw_resumen_comercial`

## Resultado confirmado por ejecución en pgAdmin

| Indicador | Valor exacto |
|---|---:|
| total_movimientos | 1.033.036 |
| ventas_brutas_gbp | 19.643.861,637 |
| abonos_mercancia_gbp | -716.462,57 |
| ventas_netas_gbp | 18.927.399,067 |
| unidades_vendidas | 11.188.061 |
| facturas_venta | 39.516 |
| clientes_compradores | 5.852 |
| fecha_minima | 2009-12-01 07:45:00 |
| fecha_maxima | 2011-12-09 12:50:00 |

**Estado:** vista creada y consultada satisfactoriamente; importes conciliados con el diagnóstico anterior (diferencia 0). 

## Próximo trabajo: dashboard existente de Power BI

1. Abrir el archivo `.pbix` actual (si existe) y confirmar qué tablas/vistas están cargadas.
2. Revisar los indicadores del dashboard y su comportamiento bajo los segmentadores existentes.
3. Si se requiere un resumen global fijo, conectar `public.vw_resumen_comercial` mediante PostgreSQL. Esta vista solo devuelve el total general y **no** reemplaza medidas dinámicas calculadas sobre `public.base_movimientos` bajo filtros de fecha/producto/cliente.
4. Registrar capturas y diferencias funcionales; corregir únicamente lo necesario.

**Pendiente por confirmar:** existencia y estado del `.pbix` del usuario. No se afirma que esté finalizado.
