# V18 — Construcción de página «Inteligencia comercial» en Power BI Desktop

## 1. Preparación (sin alterar el dashboard anterior)
1. Abre `etapa_01_postgresql_powerbi/powerbi/Dashboard_Comercial_Retail_V01.pbix`.
2. **Archivo > Guardar como** `Dashboard_Comercial_Retail_V18.pbix` dentro de `etapa_06_powerbi_portafolio/powerbi/` (carpeta privada).
3. No reescribas el PBIX original: V17 y sus archivos quedan intactos.
4. Genera los CSV con `--from-json` o `--live` según `02_ejecucion_v18.md`.

## 2. Obtener datos
Power BI Desktop > Inicio > Obtener datos > Texto/CSV: importa individualmente los cinco archivos `v18_*.csv` de `etapa_06_powerbi_portafolio/salidas`.
En Transformar datos, define separador **coma** y codificación **UTF-8**. En los campos numéricos aplica **tipo decimal usando configuración regional Inglés (Estados Unidos)** si se requiere. Mantén los códigos de producto como **texto** (p. ej. `85123A`). Las columnas `fecha_generacion_utc` se pueden dejar texto para evitar problemas de tipo.

Nombre de las tablas en Power BI (renombra con exactitud):
- `v18_kpis`
- `v18_abc`
- `v18_top_productos`
- `v18_alertas`
- `v18_calidad`

**Evita conectar** `v18_alertas[codigo_producto]` directamente a la tabla histórica `base_movimientos` porque los registros de productos se multiplicarían si se usaran relaciones many-to-many o bidireccionales. Para esta primera página, usa los datasets V18 como tablas de resumen independientes. Más adelante puede añadirse una dimensión de producto única si se necesita filtrar todo el informe de forma cruzada.

## 3. Página nueva — «Inteligencia comercial» (lienzo 16:9, 1280 × 720 recomendado)
- Encabezado 0–90 px: título `INTELIGENCIA COMERCIAL` y subtítulo `Portafolio retail 2009–2011 · análisis histórico`.
- Fila KPI (y=110–220 px): tarjetas Ventas netas; Tasa de abonos; Productos ABC; Alertas activadas.
- Izquierda (x=32–620, y=250–500): gráfico de columnas ABC: eje `categoria_abc`, valores `ventas_netas_positivas_gbp`; etiqueta alternativa `participacion_pct`.
- Derecha (x=650–1248, y=250–500): tabla Top 10: `descripcion`, `ventas_netas_gbp`, `tasa_abonos_pct`, `categoria_abc`.
- Inferior (x=32–1248, y=525–690): tabla de acciones: `id_alerta`, `severidad`, `evidencia`, `accion_sugerida`.
- Pie: etiqueta visible `Datos históricos · Reglas deterministas · Sin predicción/causalidad`.

Puedes ocultar la columna `limitacion` de la vista principal, pero incluirla en un tooltip o en una página de metodología. No ocultar las limitaciones del proyecto.

## 4. Formato y semántica
- GBP para ventas y abonos; 2 decimales en tablas y unidades abreviadas (M) en tarjetas.
- Las tasas de V18 ya están en escala **0–100**, NO en escala 0–1. En Power BI usa un formato personalizado `0.00\"%\"` (o texto con `FORMAT([Medida],"0.00") & "%"`); no apliques el formato nativo % directamente, porque multiplica por 100.
- ABC se calcula sobre **ventas netas positivas** y no equivale a las ventas netas globales.
- El Top 10 representa solo diez productos; no usarlo como suma global ni denominador ABC.
- En un panel de control, no presentar las severidades como diagnóstico clínico, riesgo probabilístico, fallo confirmado ni predicción.

## 5. Actualizar
- Reejecutar `exportar_powerbi.py --from-json ...` para exportar un nuevo JSON V17, o `--live` para consultar fuentes.
- En Power BI: Inicio > Actualizar. El `.pbix` debe conservar la misma ruta local de CSV.
- Guardar el `.pbix` V18 localmente; **no publicarlo en GitHub** antes de revisar los datos/archivos que contiene.
