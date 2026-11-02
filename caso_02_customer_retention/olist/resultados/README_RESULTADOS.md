# Resultados — Olist | Caso 2

Archivos CSV con **resultados agregados efectivamente obtenidos de las consultas PostgreSQL** durante el desarrollo del caso. Valores numéricos en notación decimal con punto y CSV separado por comas, codificación UTF-8 con BOM (compatible con Excel). Los CSV no contienen datos personales ni registros transaccionales individuales.

## Archivos

- `01_indicadores_generales.csv`: 96.478 pedidos entregados; 93.358 compradores; ventas de productos excluyendo fletes.
- `02_retencion_ponderada.csv`: retención exacta en M1, M3 y M6 sobre cohortes elegibles.
- `03_rfm_resumen.csv`: medias de recencia, frecuencia y monetario.
- `04_segmentos_clientes.csv`: segmentación exploratoria usando un umbral de 90 días, con fecha de corte histórica.
- `05_comparacion_resumen.csv`: indicadores agregados de ambos datasets, **sin combinar sus registros**.

## Alcance y limitaciones

- Olist: pedidos con estado `delivered`, `customer_unique_id` como identidad de comprador, importe de artículos (`price`) sin flete. Fecha histórica de última compra 2018-08-29.
- Online Retail II: movimientos con `incluir_recompra = 1`, compradores por `cliente_id` y facturas por `factura`; tiene reglas de negocio y período distintos.
- La retención mensual M1/M3/M6 evalúa actividad en el mes exacto, **no** retención acumulada. M1, M3 y M6 utilizan poblaciones de cohortes distintas. Para Olist se consideró julio de 2018 como el último mes completo de observación.
- No atribuir a las diferencias de recompra/retención causas específicas ni presentar comparaciones como experimento controlado.
- Los cuatro segmentos de Olist dependen de recencia histórica y un umbral heurístico de 90 días; **no** representan estado actual de clientes.
- Los datos de cohortes individuales no se han exportado; `06_exportar_detalle_cohortes.sql` permite consultarlos y exportarlos desde pgAdmin cuando se necesiten.

## Fuente

Olist Brazilian E-Commerce Public Dataset (Kaggle): https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Online Retail II: conjunto histórico analizado en el Caso 2 del mismo repositorio.
