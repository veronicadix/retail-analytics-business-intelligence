# Caso 2 — Customer Retention & Revenue Growth

## Resumen ejecutivo

Análisis de comportamiento de clientes para un conjunto histórico de transacciones de **Online Retail II** (diciembre de 2009 a diciembre de 2011). Se combina **segmentación RFM**, **cohortes de adquisición**, **frecuencia y tiempos entre compras** y una **regla exploratoria de recompra retrasada** para apoyar decisiones de retención basadas en datos. No se implementaron campañas reales ni se estimó su impacto causal.

## Pregunta empresarial

¿Qué clientes concentran valor, cómo evoluciona la actividad posterior a su primera compra y qué grupos conviene evaluar para acciones de fidelización o reactivación?

## Tecnologías

- PostgreSQL y SQL: métricas, cohortes, vistas, percentiles y ventanas analíticas.
- Python (Pandas, Matplotlib, Seaborn) y Jupyter: análisis exploratorio y visualización.
- Git/GitHub: documentación y trazabilidad del caso.

## Datos y alcance

- **5.852 clientes** identificados en la segmentación RFM.
- Compras netas históricas asociadas a estos clientes: **aprox. £16,36 millones**.
- **25 cohortes mensuales** de adquisición; la matriz de seguimiento de 0 a 6 meses contiene **147 registros observables**.
- La última fecha disponible es diciembre de 2011, mes incompleto: para comparaciones mensuales se usan períodos observables hasta noviembre de 2011.
- Los importes de esta población no equivalen necesariamente a los indicadores globales de ventas del Caso 1, pues difieren en alcance y elegibilidad.

## Resultados principales

| Indicador | Resultado |
|---|---:|
| Champions | 1.278 clientes; aprox. **69,1 %** del valor neto identificado |
| At Risk - High Value | 333 clientes |
| Hibernating | 1.511 clientes |
| Retención ponderada mes 1 | **23,34 %** (23 cohortes elegibles) |
| Retención ponderada mes 3 | **24,98 %** (21 cohortes elegibles) |
| Retención ponderada mes 6 | **22,17 %** (18 cohortes elegibles) |
| Intervalos consecutivos analizados | **30.742** en **4.234** clientes con recompra |
| Mediana entre compras | **25,03 días** |
| Promedio entre compras | **52,12 días** |
| Percentiles 75 y 90 | **62,08** y **135,97 días** |
| Recompra retrasada, regla final | **892 clientes**; aprox. **£2,42 millones** de valor neto histórico |

### Grupos propuestos para estudio de reactivación

| Segmento con recompra retrasada | Clientes | Compras netas históricas |
|---|---:|---:|
| At Risk - High Value | 306 | £924.156,50 |
| Loyal Customers | 209 | £815.236,41 |
| Champions | 34 | £332.892,98 |
| At Risk | 303 | £311.117,08 |
| Needs Attention | 40 | £38.061,54 |
| **Total** | **892** | **£2.421.464,51** |

**Prioridad de análisis:** estudiar primero los **306 At Risk - High Value** y **209 Loyal Customers** con recompra retrasada (515 clientes; cerca de **£1,74 millones** de compras netas históricas combinadas). Este importe **no** es una previsión de ingresos recuperables.

## Método resumido

1. Identificar facturas elegibles para recompra y clientes con identificador válido.
2. Construir puntuaciones R, F y M mediante `NTILE(5)` y asignar siete segmentos comerciales.
3. Agrupar clientes por mes de primera compra y medir actividad mensual no consecutiva hasta seis meses.
4. Calcular intervalos entre facturas sucesivas por cliente con `LAG` y percentiles.
5. Señalar **recompra retrasada** cuando hay al menos dos intervalos históricos y la recencia supera tanto 30 días como el doble de la mediana individual; se aplica exactamente la condición `recencia > GREATEST(30, 2 × mediana)`.

Las decisiones, supuestos y advertencias se amplían en [`METODOLOGIA.md`](METODOLOGIA.md).

## Visualizaciones

Generadas en `visualizaciones/`:

1. `01_cohort_retention_heatmap.png` — mapa de calor de cohortes.
2. `02_rfm_customer_distribution.png` — clientes por segmento.
3. `03_rfm_revenue_contribution.png` — contribución neta por segmento.
4. `04_rfm_recency_frequency.png` — comparación de recencia y frecuencia promedio (revisar superposición de etiquetas antes de la publicación definitiva).
5. `05_reactivation_opportunities.png` — valor neto histórico de grupos con recompra retrasada.

## Organización de entregables

```text
caso_02_customer_retention/
├── datos/                 # CSV derivados; revisar política de publicación de datos
├── sql/                   # 5 definiciones de vistas y README_SQL.txt
├── python/                # analisis_retencion.ipynb
├── visualizaciones/       # 5 PNG
├── resultados/            # Caso_02_Informe_Ejecutivo_Retencion_ES.docx
└── documentacion/
    ├── README_ES.md
    ├── README_EN.md
    └── METODOLOGIA.md
```

Las vistas SQL dependen de objetos preexistentes del Caso 1 (`facturas_venta` y `vw_valor_clientes`). Ejecutar en el orden indicado en el README de la carpeta SQL, con esas dependencias previamente disponibles.

## Recomendaciones

- Diseñar una prueba piloto **con grupo de control** para los segmentos priorizados.
- Comparar resultados por respuesta, recompra incremental, margen y costo de contacto; no inferir causalidad del análisis descriptivo.
- Validar la sensibilidad de las alertas a los umbrales y a la segmentación RFM antes del uso operativo.

## Limitaciones y estado

- Dataset histórico; las etiquetas «en riesgo» y «retrasada» describen el período analizado, no el estado actual de clientes reales.
- `NTILE(5)` puede separar clientes empatados entre quintiles; las puntuaciones son relativas.
- No se dispone de experimentos de marketing ni de costos de campañas para estimar retorno.
- Las retenciones por horizonte se calculan con cohortes elegibles distintas y no implican abandono definitivo.
- **Olist es una extensión pendiente:** debe analizarse como fuente y modelo separados; no se ha unido a Online Retail II ni se han producido hallazgos comparables todavía.

## Informe ejecutivo

Véase `resultados/Caso_02_Informe_Ejecutivo_Retencion_ES.docx`.
