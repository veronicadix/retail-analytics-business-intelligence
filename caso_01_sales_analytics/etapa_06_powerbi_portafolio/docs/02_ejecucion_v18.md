# Guía rápida V18 (Windows CMD)

## A — Reutilizar JSON V17 ya generado (opción recomendada: sin consultas)
Situarte dentro de `proyecto-ventas-gcp-ai V18`:

```cmd
cd /d "C:\ruta\a\Portafolio_Data_Engineering\proyecto-ventas-gcp-ai V18"
```

Crear entorno e instalar dependencias **solo si aún no existe `.venv`** (el modo JSON necesita solo Python estándar):

```cmd
python etapa_06_powerbi_portafolio\python\exportar_powerbi.py --from-json "..\proyecto-ventas-gcp-ai V17\etapa_05_inteligencia_comercial\salidas\inteligencia_comercial_20261023_114428.json"
```

El archivo JSON se crea en el PC del usuario tras correr V17 y **no se empaqueta** en la distribución V18 por privacidad. Si tiene otro nombre, sustituir solo ese nombre por el archivo real que muestra Explorador.

## B — Obtener datos actualizados de las fuentes (opcional)
```cmd
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r etapa_03_automatizacion\requirements.txt
.venv\Scripts\python.exe -m pip install -r etapa_04_claude_api\requirements.txt
copy "..\proyecto-ventas-gcp-ai V17\.env" ".env"
.venv\Scripts\python.exe etapa_06_powerbi_portafolio\python\exportar_powerbi.py --live
```

`--live` hace consultas de **solo lectura** a PostgreSQL/BigQuery. `--from-json` no consulta bases de datos, no requiere `.env` ni librerías externas.

## Archivos de salida
Generados en `etapa_06_powerbi_portafolio\salidas`:
- `v18_kpis.csv`: indicadores financieros y calidad agregados
- `v18_abc.csv`: categorías A/B/C por códigos únicos y base positiva
- `v18_top_productos.csv`: top diez, tasas y clasificación ABC
- `v18_alertas.csv`: 4 alertas V17 con evidencias, acciones y límites
- `v18_calidad.csv`: conciliación, mapeo y granularidad
- `v18_manifest.json`: origen, fecha y advertencias

**Estas exportaciones están excluidas del repositorio GitHub.** No sobrescribir la automatización de V15, ni V16/V17 originales. Consulta `01_powerbi_paso_a_paso.md` para construir la página.
