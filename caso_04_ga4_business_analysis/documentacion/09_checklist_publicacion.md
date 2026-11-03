# Caso 04 — Checklist de publicación en GitHub

## Antes del commit

- [ ] Copiar `README_caso_04_ES.md` y guardarlo como `caso_04_ecommerce_conversion/README.md`.
- [ ] Copiar `README_EN.md` a `caso_04_ecommerce_conversion/README_EN.md`.
- [ ] Confirmar los tres `.sql` en `sql/` y los tres `.csv` en `resultados/`.
- [ ] Confirmar los documentos `04`, `05`, `07` y `08` en sus carpetas correspondientes.
- [ ] Confirmar los dos archivos BPMN importables (y opcionalmente `.bpm` nativos para edición local).
- [ ] Revisar visualmente ambos diagramas en Bizagi y exportar PNG a `visualizaciones/` cuando estén correctos.
- [ ] Abrir el README local y comprobar que todos los enlaces relativos correspondan a archivos existentes.
- [ ] Inspeccionar cambios para evitar subir credenciales, archivos temporales, bases privadas o datos personales.
- [ ] Verificar que no se hayan modificado accidentalmente los casos 01–03 ni el README principal del repositorio.

## GitHub Desktop

1. Abrir el repositorio `retail-analytics-business-intelligence`.
2. Revisar la pestaña **Changes** y marcar solo los archivos del Caso 04 que deban publicarse.
3. **Summary:** `docs: add case 04 GA4 funnel analysis and BA deliverables`.
4. **Description:** `Add BigQuery SQL and results, business findings, BRD, AS-IS/TO-BE BPMN, Agile user stories, UAT test design, and bilingual case README.`
5. Seleccionar **Commit to main** (o a la rama de trabajo que estés usando).
6. Pulsar **Push origin**.
7. Abrir el repositorio en GitHub y entrar a `caso_04_ecommerce_conversion/README.md`. Comprobar la vista previa, enlaces y archivos.

## Estado editorial

- Análisis SQL realizado con datos públicos históricos y ofuscados.
- Requerimientos e historias: propuesta de solución, no implementación.
- UAT: 31 escenarios diseñados y **No ejecutados**.
- BPMN AS-IS: modelo conceptual reconstruido a partir de eventos, no proceso verificado de una empresa.
