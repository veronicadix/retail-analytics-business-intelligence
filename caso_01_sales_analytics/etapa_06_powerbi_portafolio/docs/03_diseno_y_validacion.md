# Diseño de dashboard V18 — contrato y aceptación

**Preguntas de negocio:** ¿En qué productos concentrar el análisis comercial? ¿Qué señales justifican revisar abonos? ¿Qué limitaciones condicionan las conclusiones?

**Grupos de visualización:** cuatro KPIs; ventas positivas por ABC; ranking Top 10; bandeja de alertas; ficha de límites y calidad.

**Criterios de aceptación después de importar CSV en Power BI**:
1. Ventas netas = GBP 18,927,399.07 (instantánea V17 2026-10-23).
2. Productos ABC = 4,705; categorías 1,038/1,257/2,410.
3. Participación A 80.01%, B 14.99%, C 5.00%.
4. 4 alertas: CONCENTRACION_A, ABONOS_22423, PERIODO_PARCIAL, GRANULARIDAD.
5. PRODUCTO 22423 tasa 5.00%; tasa global 3.65% (comparar tasas en puntos %).
6. Al menos una nota visible: **2009-2011 histórico, diciembre de 2011 incompleto**.
7. Distinguir base ABC positiva (GBP 18,927,963.33) de ventas netas globales (GBP 18,927,399.07), diferencia GBP 564.26.
8. Los códigos de producto mantienen tipo texto.

**Esta V18 no crea ni modifica automáticamente un archivo PBIX**: se entrega el archivo V01 preexistente y pasos para guardar una copia V18 editable dentro de Power BI Desktop. Verificación de diseño y resultado final requiere Power BI en Windows.
