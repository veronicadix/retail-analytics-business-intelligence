# V07 — Cierre de validaciones esenciales y paso siguiente

Fecha: 2026-10-16  
Base PostgreSQL: `portafolio_retail`

## Control ejecutado

Archivo: `sql/03_validaciones/05_coherencia_flags.sql`.

Resultados (en el orden de columnas del SELECT):

| Indicador | Resultado |
|---|---:|
| Líneas con ambos flags | 0 |
| Ventas con importe no positivo | 0 |
| Abonos con importe no negativo | 0 |
| Flags comerciales fuera de mercancía | 0 |
| Importe solapado GBP | 0 |

**Estado:** aprobado. También están registrados los controles de nulidad, duplicados y conciliación de importes en documentación V04–V06. No se repetirán salvo que cambien datos o lógica.

## Próximo trabajo útil: documentar transformaciones ya implementadas

Antes de tocar SQL productivo, identificar las definiciones de las seis vistas existentes y su lógica. Ejecutar `sql/01_diagnostico/06_definiciones_vistas.sql` (solo lectura) y guardar las definiciones obtenidas en el repositorio; después contrastar las vistas que alimentan el dashboard y resolver solo las brechas detectadas.

## Política de trabajo

- Una prueba por riesgo real, no una sucesión de verificaciones redundantes.
- Prioridad: modelo comercial terminado, dashboard funcional, BigQuery, automatización, Claude API.
- Conservar código comentado, versión y resultado verificable.
