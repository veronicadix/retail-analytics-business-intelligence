# Reglas de negocio — Etapa 1

| ID | Regla / campo | Estado | Evidencia / validación |
|---|---|---|---|
| RB-01 | Ventas brutas = suma de `importe_gbp` cuando `incluir_ventas_brutas = 1` | Conciliado 2026-10-16 | `sql/02_validaciones/01_reconciliacion.sql` |
| RB-02 | Abonos = suma de `importe_gbp` cuando `incluir_abonos_mercancia = 1`, manteniendo signo | Conciliado 2026-10-16 | mismo SQL |
| RB-03 | Ventas netas = ventas brutas + abonos (negativos) | Conciliado 2026-10-16 | mismo SQL |
| RB-04 | Unidades = suma de `cantidad` cuando `incluir_demanda_unidades = 1` | Por validar | comparar contra tarjeta Power BI |
| RB-05 | Facturas de ventas = cantidad distinta de `factura` con `incluir_ventas_brutas = 1` | Por validar | comparar contra tarjeta Power BI |
| RB-06 | Compradores = clientes distintos identificados para `incluir_recompra = 1` | Por precisar | confirmar elegibilidad y nulos de `cliente_id` |

## Valores de referencia previamente registrados (no son nuevas comprobaciones)
- Ventas brutas: **19.643.861,64 GBP**
- Abonos: **−716.462,57 GBP**
- Ventas netas: **18.927.399,07 GBP**

**Importante:** verificar que origen, filtros, intervalo temporal y actualización de Power BI sean equivalentes antes de exigir igualdad.
