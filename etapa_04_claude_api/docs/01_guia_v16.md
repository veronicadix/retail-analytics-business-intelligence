# V16 — Informe comercial con IA opcional

## Alcance
Se mantiene íntegra la V15. El Programador de tareas instalado en V15 **continúa apuntando a V15**: no se altera ni migra automáticamente a V16.

La V16 consulta únicamente las vistas existentes `vw_resumen_comercial` y `vw_producto_mes` en BigQuery, genera un Markdown local trazable y permite usar Claude API opcionalmente. Nunca envía datos crudos de clientes.

## CMD (Windows) — comandos separados
```cmd
cd /d "C:\ruta\a\Portafolio_Data_Engineering\proyecto-ventas-gcp-ai V16"
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r etapa_04_claude_api\requirements.txt
.venv\Scripts\python.exe etapa_04_claude_api\python\informe_comercial.py --local
```

Se requiere `gcloud auth application-default login` previamente configurado en el usuario Windows que corre V16 (V15 ya accedía a BigQuery). NO repetir autenticación si funciona. No es necesario `.env` para generar informes locales de BigQuery. Si ejecutas también el pipeline de la etapa 3 en V16, copia tu `.env` local de V15 a V16; nunca lo subas a GitHub.

**Resultado:** `etapa_04_claude_api\salidas\informe_comercial_FECHA.md`. El nombre incluye fecha y hora, sin sobreescribir informes anteriores.

## Uso Claude (opcional; requiere créditos API)
Sin instalar Claude Pro. En CMD, abrir primero `set ANTHROPIC_API_KEY=...` temporalmente en tu equipo (**no enviar la clave al chat**) y correr:
```cmd
.venv\Scripts\python.exe etapa_04_claude_api\python\informe_comercial.py --claude
```
No se programa esta llamada ni se ejecuta automáticamente. Una ejecución invoca una solicitud a la API, con costo por tokens. El modelo predeterminado es configurable mediante `ANTHROPIC_MODEL`; si el modelo deja de estar disponible, seleccionar uno vigente en Anthropic Console.

## Seguridad y limitaciones
- Sin acceso a red aquí: las consultas no se han ejecutado contra tu cuenta. La sintaxis Python fue validada localmente.
- La salida Markdown local puede contener cifras de negocio: no publicar automáticamente.
- Recomendaciones deterministas no prueban causalidad; tampoco el modelo IA.
- Dataset histórico 2009-2011; no atribuirlo a un negocio actual.
- Consultas BigQuery pueden consumir cuota, aunque la API de Claude no se use.
- No mezclar los logs de la tarea V15 con los resultados V16.
