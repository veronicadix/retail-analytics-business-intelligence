# V17 — Inteligencia comercial y recomendaciones automatizadas

## Alcance
Motor **determinista**, sin coste de Claude API, que genera archivos Markdown, JSON y CSV a partir de las **vistas agregadas** BigQuery y `public.vw_pareto_productos` de PostgreSQL. Cero escrituras en las bases de datos.

## Preparación (CMD dentro de la carpeta V17)
```cmd
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt
.venv\Scripts\python.exe -m pip install -r etapa_04_claude_api\requirements.txt
.venv\Scripts\python.exe -m pip install "psycopg[binary]>=3,<4" python-dotenv
copy "..\proyecto-ventas-gcp-ai V16\.env" ".env"
```
No compartir `.env` ni incluirlo en GitHub. Se requieren las credenciales locales ADC de Google Cloud ya configuradas. Si el archivo `.env` ya existe y contiene información vigente, no sobrescribirlo.

## Ejecución
```cmd
.venv\Scripts\python.exe etapa_05_inteligencia_comercial\python\motor_comercial.py --local
```
O ejecutar `etapa_05_inteligencia_comercial\ejecutar_inteligencia_local.cmd`.

## Archivos de salida
En `etapa_05_inteligencia_comercial\salidas`: informe `.md`, evidencia completa `.json` y alertas `.csv` (UTF-8 BOM para Excel).

## Reglas
- Concentración A: alerta informativa si A concentra al menos 75% de la base positiva.
- Abonos: alerta para productos top 10 cuya tasa de abonos supera la tasa global en **al menos 1 punto porcentual**.
- Período parcial: advertencia cuando la cobertura termina el 9 de diciembre de 2011.
- Catálogo: alertas por códigos del top 10 sin mapeo y filas duplicadas consolidadas.

Los umbrales son **supuestos de demostración ajustables**, no límites reglamentarios ni evidencia de problemas de calidad.

## Limitaciones y controles
- **No** usa datos personales ni llama Claude; no hace pronósticos ni causalidad.
- ABC usa saldos positivos en PostgreSQL, no el total neto global de BigQuery; se informa la diferencia.
- Se agrupan códigos duplicados de la vista PostgreSQL antes de calcular ABC.
- El informe no debe inferir condiciones comerciales actuales de transacciones 2009–2011.
- Las salidas se excluyen de GitHub; revisar antes de publicar.
- **V15** permanece como tarea semanal activa en el computador, sin modificaciones. **V16** permanece intacta en su carpeta original.
