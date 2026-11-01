CASO 2 - Customer Retention & Revenue Growth

SQL reproducible de las cinco vistas, extraido y reformateado a partir de las
definiciones pg_views compartidas por la usuaria (no son cambios metodologicos).

EJECUTAR EN ORDEN (si se reconstruye la base desde el Caso 1):
01_rfm_clientes.sql (requiere public.vw_valor_clientes)
02_cohortes_retencion.sql (requiere public.facturas_venta)
03_matriz_retencion.sql (requiere vw_cohortes_retencion)
04_intervalos_recompra.sql (requiere public.facturas_venta)
05_oportunidades_reactivacion.sql (requiere vw_intervalos_recompra y vw_rfm_clientes)

Si las vistas ya existen y funcionan, NO es necesario volver a ejecutarlas.
Copiar los archivos a caso_02_customer_retention/sql/ y versionar en GitHub.

Limitaciones:
- La RFM monetaria clasifica por compras brutas, no netas.
- NTILE puede dividir empates.
- Retencion mensual NO consecutiva.
- Se excluye diciembre 2011 de la matriz por ser un mes parcial.
- La regla de recompra retrasada es exploratoria.
- Los importes historicos NO son beneficios o ventas futuras atribuibles.
