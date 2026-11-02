# Caso 03 | Pronóstico de demanda y planificación de inventario

**Retail Analytics & Business Intelligence | Proyecto de portafolio**

## Problema de negocio
Una empresa minorista necesita anticipar las unidades demandadas por tienda y producto y evaluar el compromiso entre disponibilidad de producto e inventario adicional. El proyecto transforma series históricas de ventas en pronósticos, diagnósticos de demanda y escenarios **hipotéticos** de reposición.

## Datos y alcance
- **Fuente:** conjunto M5 Forecasting Accuracy (ventas históricas de Walmart, publicado para la competencia M5).
- **Período histórico de entrenamiento y análisis:** 29/01/2011–24/04/2016 (1.913 días en `sales_train_validation.csv`).
- **Series:** 30.490 combinaciones producto-tienda; 10 tiendas y 3 categorías.
- **Prueba final independiente:** 28/03/2016–24/04/2016 (`d_1886`–`d_1913`, 28 días).
- **Archivos de entrada:** `sales_train_validation.csv`, `calendar.csv` y `sell_prices.csv`.

> Las ventas del M5 son datos históricos; los stocks, pedidos, lead time, costos y políticas de reposición de este caso **no son operaciones observadas de Walmart**.

## Metodología
1. **Exploración y calidad:** series históricas, ventas por tienda y categoría, tendencia, comportamiento semanal y comprobaciones de nulos.
2. **Pronóstico agregado:** comparar Naive 7, media móvil de 28 días y promedio del mismo día de la semana en las últimas ocho semanas (`Dia_semana_8s`). Probar una tendencia semanal con validación temporal.
3. **Pronóstico tienda-categoría:** 30 segmentos, validación temporal y comparación de políticas.
4. **Pronóstico producto-tienda:** 30.490 series, con evaluación de errores a nivel granular.
5. **Diagnóstico de intermitencia:** ADI y CV² sobre una ventana histórica de 168 días; comparación del método semanal y Croston-SBA.
6. **Simulación de inventario:** revisión semanal, lead time de siete días, inventario inicial supuesto equivalente a 14 días de pronóstico medio y comparación de 0 contra 7 días de buffer adicional.
7. **Sensibilidad económica:** comparar costos supuestos de mantener inventario y de demanda insatisfecha, sin afirmar rentabilidad real.

## Resultados predictivos

| Nivel / política | WAPE | Interpretación |
|---|---:|---|
| Agregado, `Dia_semana_8s` | **5,52 %** | Mejor baseline agregado evaluado |
| Agregado, tendencia semanal | 6,55 % | No supera baseline |
| Tienda-categoría, `Dia_semana_8s` | **9,33 %** | Mejor política segmentada global |
| Tienda-categoría, selección por validación | 9,52 % | No mejora usar el mismo método para los 30 segmentos |
| Producto-tienda, `Dia_semana_8s` | **76,217 %** | Pronóstico granular significativamente más difícil |
| Producto-tienda, Croston-SBA α=0,1 | 78,1035 % | No mejora resultado global |
| Producto-tienda, Croston-SBA α=0,2 | 78,5082 % | No mejora resultado global |

**Precaución:** los WAPE agregados, segmentados y producto-tienda no son directamente equivalentes: la compensación de errores entre series cambia con el nivel de agregación.

### Patrones de demanda
- Intermitente: 22.986 series (75,39 %).
- Irregular intermitente: 3.176 (10,42 %).
- Regular: 3.295 (10,81 %).
- Errática: 703 (2,31 %).
- Sin demanda histórica positiva en ventana analizada: 330 (1,08 %).

El 85,81 % de las series se clasificó como intermitente o irregular intermitente usando los umbrales descriptivos ADI=1,32 y CV²=0,49.

## Simulación de reposición (28 días)

| Métrica | Sin buffer | Buffer de 7 días |
|---|---:|---:|
| Demanda histórica de prueba | 1.183.626 | 1.183.626 |
| Demanda atendida simulada | 985.097 | 1.107.316 |
| Demanda no atendida simulada | 198.529 | 76.310 |
| **Fill rate simulado** | **83,23 %** | **93,55 %** |
| Unidades ordenadas simuladas | 759.451 | 1.139.915 |
| Inventario final simulado | 119.777 | 356.190 |
| Inventario medio simulado | 269.815 | 458.951 |

**Intercambio principal:** el buffer atiende **122.219 unidades adicionales** (+10,32 puntos porcentuales en fill rate), a costa de **189.136 unidades adicionales de inventario medio** (+70,10 % aproximadamente).

### Supuestos operativos
- Tiempo de entrega fijo: 7 días; inventario revisado cada 7 días.
- Inventario inicial hipotético: demanda prevista media de 14 días por producto-tienda.
- Buffer adicional: 0 o 7 días de demanda prevista.
- Demanda no atendida se pierde, no se acumula como pedido pendiente.
- Proveedor con capacidad ilimitada y sin restricciones presupuestarias.

## Análisis económico ilustrativo

La comparación se basa en:

`costo_total = inventario_medio × costo_mantener_unidad_28d + demanda_no_atendida × costo_faltante_unidad`

| Costo de mantener una unidad durante 28 días | Costo de faltante de equilibrio por unidad |
|---:|---:|
| US$0,10 | US$0,1548 |
| US$0,50 | US$0,7738 |
| US$1,00 | US$1,5475 |
| US$2,00 | US$3,0950 |

En 13 de las 16 combinaciones de costos simulados, el escenario con buffer presentó menor costo según **esta fórmula limitada**. El análisis excluye costo de compra, margen real, costo de pedidos, capital, descuentos y caducidad. **No calcula ganancias ni ahorro reales y no optimiza inventarios.**

## Estructura del caso

```text
caso_03_demand_forecasting/
├── datos/
│   ├── raw/           # CSV originales (descarga externa; no subir datasets grandes)
│   └── procesados/
├── documentacion/     # Informe de negocio y metodología
├── python/            # Scripts 01 a 10
├── resultados/        # CSV y JSON generados
├── sql/               # Reservada para consultas futuras
├── visualizaciones/   # Gráficos generados
├── README.md           # Esta presentación
└── README_EN.md        # English version
```

## Reproducción
1. Descargar el dataset en [Kaggle M5 Forecasting Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data), aceptando sus términos de uso.
2. Descomprimir los CSV necesarios en `datos/raw/`.
3. Instalar dependencias: `python -m pip install pandas numpy matplotlib`.
4. Desde la carpeta del Caso 3, ejecutar los scripts numerados en `python/` en orden del **01 al 10**.
5. Inspeccionar `resultados/` y `visualizaciones/` para revisar las métricas y gráficos generados.

> Reproducibilidad: verificar y fijar versiones de dependencias antes de la publicación final. No publicar ZIP, datos masivos ni credenciales. Mantener CSV/JSON de resultados pequeños y visualizaciones útiles para evidenciar los hallazgos.

## Limitaciones y siguientes mejoras
- El WAPE por producto-tienda es alto: no debe usarse directamente como prueba de precisión de pedidos individuales.
- El histórico de ventas puede reflejar restricciones de disponibilidad no observadas; ventas no siempre equivalen a demanda no restringida.
- Faltan existencias reales, costos completos, restricciones de proveedor y calibración de inventario de seguridad.
- Los resultados son de **un período final de 28 días** y requieren monitoreo y validación adicional antes de uso operativo.
- Extensiones posibles: evaluación multiventana, ajuste de políticas por grupo de demanda, lead time variable y optimización bajo restricciones reales.

## Herramientas y competencias
Python · pandas · NumPy · Matplotlib · Time Series Forecasting · WAPE / MAE · Demand Segmentation (ADI / CV²) · Inventory Planning · Business Analysis · Sensitivity Analysis
