# Evidencia de resultados y limitaciones

Fecha del corte de la demostración V17/V18: 23 de octubre de 2026 (generación de indicadores 16:44 UTC). Periodo de transacciones: 2009-12-01 07:45:00 a 2011-12-09 12:50:00.

| Métrica | Resultado |
|---|---:|
| Ventas netas | GBP 18.927.399,07 |
| Ventas brutas | GBP 19.643.861,64 |
| Abonos | GBP -716.462,57 |
| Facturas | 39.516 |
| Unidades | 11.188.061 |
| Porcentaje abonos / bruto | 3,65 % |
| Base ABC de códigos con neto positivo | GBP 18.927.963,33 |
| Diferencia entre base ABC y neto global | GBP 564,26 |

## Pareto por código único

| Grupo | Códigos | Ventas netas positivas GBP | Participación |
|---|---:|---:|---:|
| A | 1.038 | 15.144.137,86 | 80,01 % |
| B | 1.257 | 2.838.241,75 | 14,99 % |
| C | 2.410 | 945.583,72 | 5,00 % |

## Alertas documentadas

1. `CONCENTRACION_A`: 80,01 % de base positiva concentrada en A; revisar margen/disponibilidad, sin concluir que haya que comprar más.
2. `ABONOS_22423`: producto 22423 con 5,00 % abonos frente al 3,65 % general; inspeccionar transacciones y causas, no atribuir defectos.
3. `PERIODO_PARCIAL`: excluir diciembre 2011 de comparaciones de meses completos.
4. `GRANULARIDAD`: 170 filas adicionales consolidadas, que no son 170 códigos duplicados.

**Alcance:** alertas descriptivas y metodológicas, no predicciones, causalidad ni decisiones comerciales autorizadas. El origen del dataset y su licencia deben confirmarse antes de distribuir datos o capturas derivadas.
