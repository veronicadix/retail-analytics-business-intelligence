# Visualizaciones Olist — Caso 2

Este paquete genera visualizaciones PNG a partir de los CSV ubicados en `olist/resultados`.

## Archivos esperados en `olist/resultados`
- `01_indicadores_generales.csv`
- `02_retencion_ponderada.csv`
- `04_segmentos_clientes.csv`
- `05_comparacion_resumen.csv`
- Opcional: `06_detalle_cohortes_olist.csv` para generar el heatmap de cohortes.

## Salidas generadas en `olist/visualizaciones`
1. `01_olist_recompra.png`
2. `02_olist_retencion_ponderada.png`
3. `03_olist_segmentos_clientes.png`
4. `04_comparacion_recompra_datasets.png`
5. `05_comparacion_retencion_datasets.png`
6. `06_olist_heatmap_cohortes.png` (solo si existe el CSV detallado de cohortes)

## Ejecución sugerida
Ubícate en la carpeta `caso_02_customer_retention/olist/python` y ejecuta:

```bat
..\..\.venv\Scripts\python.exe generar_visualizaciones_olist.py
```

Si el script queda dentro de `olist/python`, detectará automáticamente la carpeta `olist`.

## Para generar el heatmap de cohortes
1. Ejecuta `06_exportar_detalle_cohortes.sql` en pgAdmin.
2. Exporta el resultado a CSV con nombre `06_detalle_cohortes_olist.csv`.
3. Guarda ese archivo dentro de `olist/resultados`.
4. Ejecuta nuevamente el script.
