Retail Analytics | De los datos de ventas a la inteligencia comercial

Proyecto de portafolio | PostgreSQL · SQL · Python · BigQuery · Power BI

Sobre el proyecto

En este proyecto quise trabajar sobre un problema habitual en las empresas: disponer de grandes volúmenes de información comercial, pero necesitar un proceso claro para convertirlos en indicadores útiles para el negocio.

Tomé como punto de partida un conjunto de más de un millón de movimientos comerciales y desarrollé una solución que integra preparación de datos, consultas SQL, automatización con Python, análisis en BigQuery y visualización en Power BI.

El trabajo fue evolucionando por etapas. Comencé con la organización y validación de los datos en PostgreSQL, continué con su integración en BigQuery y desarrollé procesos de automatización e informes comerciales. Finalmente, construí un dashboard de siete páginas para reunir los resultados y facilitar su análisis.

Mi intención fue abordar el proyecto tanto desde el lado técnico como desde las preguntas que podría plantear un equipo comercial.

Alcance: los datos corresponden al período comprendido entre diciembre de 2009 y diciembre de 2011. Se utilizan con fines de análisis y aprendizaje. Este proyecto no representa una implementación empresarial en producción ni describe la demanda actual.

¿Qué problemas busqué resolver?

El proyecto se desarrolló alrededor de cinco preguntas de negocio:

¿Cuáles son los productos que más contribuyen a las ventas?

¿Qué artículos presentan tasas de abonos que merecen una revisión?

¿Cómo identificar clientes recurrentes y grupos con distintos comportamientos de compra?

¿Qué cambios se observan en las ventas y en las unidades comercializadas?

¿Cómo utilizar estos resultados para apoyar decisiones de planificación comercial?

Además, quería que los indicadores pudieran explicarse y rastrearse hasta sus reglas de cálculo. Por eso incorporé controles de calidad, conciliaciones y documentación de la metodología.

Arquitectura

La solución combina PostgreSQL, Python, BigQuery y Power BI.

flowchart LR
    A[PostgreSQL: datos y catálogo] --> B[Python: extracción y validación]
    B --> C[BigQuery Sandbox: staging y raw]
    C --> D[Vistas SQL: indicadores]
    A --> E[Análisis Pareto ABC]
    D --> F[Python: informes y reglas comerciales]
    E --> F
    F --> G[Indicadores y alertas]
    G --> H[Power BI: dashboard comercial]

PostgreSQL se utiliza para organizar los movimientos, aplicar reglas de negocio y crear las vistas necesarias para el análisis.

Python permite automatizar la extracción y carga de información, registrar ejecuciones y preparar informes.

BigQuery se utiliza como entorno analítico en la nube. El proceso incluye conciliaciones para comprobar que los registros coincidan con PostgreSQL.

Power BI reúne los indicadores comerciales y permite explorar los resultados mediante gráficos, tablas, medidas DAX y segmentadores.

La carga de PostgreSQL a BigQuery quedó programada semanalmente mediante Windows Task Scheduler. Es una automatización local que depende de que el computador y las conexiones estén disponibles.

Para trabajar con BigQuery Sandbox utilicé un procedimiento de reemplazo basado en copy jobs, en lugar de operaciones MERGE que requerían facturación habilitada.

Resultados principales

El conjunto histórico contiene 1.033.036 movimientos comerciales.

Después de aplicar las reglas de negocio, obtuve los siguientes resultados:

Indicador

Resultado

Movimientos analizados

1.033.036

Ventas brutas

GBP 19.643.861,64

Abonos de mercancía

GBP -716.462,57

Ventas netas

GBP 18.927.399,07

Facturas

39.516

Clientes analizados

5.852

Unidades observadas

11.188.061

Abonos sobre ventas brutas

3,65 %

Productos con ventas netas positivas en el análisis ABC

4.705

Clasificación ABC

Uno de los análisis que desarrollé fue la clasificación de productos según su contribución a las ventas netas positivas.

Categoría

Productos

Ventas netas positivas GBP

Participación

A

1.038

15.144.137,86

80,01 %

B

1.257

2.838.241,75

14,99 %

C

2.410

945.583,72

5,00 %

La categoría A concentra aproximadamente el 80 % de la base positiva analizada, por lo que representa un punto de partida para revisar la disponibilidad, el margen y el comportamiento de compra de los productos más relevantes.

Durante este análisis encontré que algunos códigos aparecían en más de una fila. Para evitar duplicidades en la clasificación, consolidé 170 filas adicionales antes de recalcular el ABC.

La base Pareto positiva es de GBP 18.927.963,33, mientras que las ventas netas globales son GBP 18.927.399,07. La diferencia de GBP 564,26 se explica porque el análisis ABC considera únicamente códigos con ventas netas positivas.

Dashboard en Power BI

El resultado visual del proyecto es un dashboard de siete páginas, diseñado para presentar los indicadores de manera ordenada y facilitar su interpretación.

01. Resumen comercial



Esta página presenta los indicadores generales de ventas brutas, abonos, ventas netas, facturas, clientes y unidades vendidas.

También incluye la evolución mensual y un segmentador de fechas para consultar distintos períodos.

02. Prioridad de productos



Aquí reuní los análisis que permiten identificar productos relevantes por ventas netas, participación ABC y recompra.

La página incluye rankings, distribución por categorías y una tabla de detalle para consultar productos específicos.

03. Crecimiento y abonos



Esta página compara el comportamiento de los productos entre enero y noviembre de 2010 y el mismo período de 2011.

Además del crecimiento porcentual, incorporé el incremento absoluto en GBP. Esta distinción es importante porque un producto puede presentar una variación porcentual muy elevada cuando sus ventas del año anterior fueron pequeñas.

También incluí un ranking por tasa de abonos. Para reducir distorsiones por ventas brutas prácticamente nulas, utilicé un umbral exploratorio mínimo de GBP 1.000 por producto.

04. Clientes y retención



El análisis de clientes incluye recurrencia de compra, ticket bruto promedio, clasificación por segmentos y rankings por valor comercial.

El objetivo es diferenciar grupos de clientes que pueden requerir estrategias de fidelización, desarrollo o reactivación.

05. Evolución y planificación



Esta página muestra la evolución mensual de unidades vendidas y la comparación de ventas netas entre 2010 y 2011.

Para mantener períodos comparables, el indicador interanual utiliza enero a noviembre de ambos años. El crecimiento obtenido fue de aproximadamente 2,33 %.

Diciembre de 2011 contiene registros únicamente hasta el día 9 y se identifica como un período parcial.

06. Calidad y metodología



Consideré importante dedicar una página a explicar cómo se construyeron los indicadores.

Incluye la clasificación de los movimientos comerciales, las reglas de inclusión, los controles de calidad y las diferencias entre los importes registrados y las ventas netas calculadas.

Los controles presentados muestran cero identificadores duplicados y cero fechas nulas.

07. Inteligencia comercial



La última página reúne indicadores de negocio, análisis ABC y cuatro alertas comerciales generadas mediante reglas.

Cada alerta incluye la evidencia que la origina, una acción sugerida y una limitación de interpretación.

Mi objetivo fue que las recomendaciones pudieran explicarse a partir de los datos, sin presentar observaciones históricas como predicciones o conclusiones definitivas.

Algunos hallazgos del proyecto

Concentración de ventas

Los 1.038 productos clasificados en la categoría A representan el 80,01 % de la base de ventas netas positivas.

Este resultado permite priorizar su revisión comercial. Sin embargo, las ventas históricas no son suficientes para recomendar incrementos de inventario sin considerar márgenes, existencias y demanda.

Abonos de mercancía

El producto 22423 — REGENCY CAKESTAND 3 TIER registró una tasa de abonos cercana al 5,00 %, superior a la tasa general del 3,65 %.

Esto constituye una señal para investigar, no una prueba de defectos del producto. Sería necesario revisar los motivos de los abonos y el volumen de transacciones.

Crecimiento interanual

Al comparar enero–noviembre de 2010 con enero–noviembre de 2011, las ventas netas aumentaron aproximadamente un 2,33 %.

Durante el análisis por producto observé que algunos crecimientos porcentuales muy altos correspondían a bases de ventas pequeñas. Por eso incorporé también el incremento monetario absoluto.

Calidad de datos

Uno de los aprendizajes más importantes fue que obtener una cifra no significa necesariamente que esté lista para utilizarse.

La clasificación de movimientos, la granularidad de las vistas y los criterios de inclusión influyen directamente en los resultados. Documentarlos permite entender por qué dos indicadores aparentemente similares pueden tener valores diferentes.

Automatización e inteligencia comercial

Además del dashboard, desarrollé un pipeline en Python para cargar información desde PostgreSQL a BigQuery.

El proceso incorpora registros de ejecución, controles para evitar ejecuciones simultáneas y una programación semanal local.

También desarrollé un informe comercial automatizado y un conjunto de reglas que generan cuatro alertas relacionadas con concentración de ventas, abonos, comparabilidad temporal y granularidad de productos.

Estas alertas no requieren un modelo de inteligencia artificial para funcionar. Se generan a partir de condiciones explícitas y métricas calculadas.

Claude API quedó contemplada como una posible ampliación del proyecto, pero no se utilizó para generar los resultados publicados.

Etapas de desarrollo

Etapa

Herramientas

Trabajo realizado

01. Preparación de datos y BI

PostgreSQL, SQL, Power BI

Organización de datos, reglas de negocio, vistas y dashboard inicial

02. Analítica en la nube

BigQuery Sandbox

Carga y conciliación de datos y vistas analíticas

03. Automatización

Python, Windows Task Scheduler

Pipeline de carga y programación semanal

04. Informes comerciales

Python

Generación local de informes; Claude API quedó como opción futura

05. Inteligencia comercial

Python

Alertas comerciales y recomendaciones basadas en reglas

06. Dashboard de portafolio

Power BI, DAX

Dashboard final de siete páginas con diseño unificado

El proyecto se desarrolló de forma incremental, conservando versiones anteriores para documentar los cambios y mantener los resultados funcionales.

Organización del repositorio

retail-analytics-business-intelligence/
│
├── README.md
├── .gitignore
├── .env.example
│
├── capturas/
│   ├── 01_resumen_comercial.png
│   ├── 02_prioridad_productos.png
│   ├── 03_crecimiento_abonos.png
│   ├── 04_clientes_retencion.png
│   ├── 05_evolucion_planificacion.png
│   ├── 06_calidad_metodologia.png
│   └── 07_inteligencia_comercial.png
│
├── docs/
├── etapa_01_postgresql_powerbi/
├── etapa_02_bigquery/
├── etapa_03_automatizacion/
├── etapa_04_claude_api/
├── etapa_05_inteligencia_comercial/
└── etapa_06_powerbi_portafolio/

Documentación técnica

Para quienes quieran revisar con mayor detalle las decisiones y los procedimientos utilizados, el repositorio incluye:

Arquitectura técnica: componentes, flujo de información y decisiones de implementación.

Resultados y limitaciones: indicadores, metodología de análisis y alcance de los resultados.

Reproducibilidad: requisitos y pasos generales para ejecutar el proyecto.

Publicación segura: criterios para preparar los archivos antes de compartirlos.

Guía para entrevistas: explicación de las decisiones técnicas y comerciales.

También se incluyen los scripts SQL, Python y las medidas DAX correspondientes a las distintas etapas.

Reproducción y limitaciones

El repositorio permite consultar el código y entender cómo se construyó la solución. Para reproducir el proceso completo es necesario disponer de una fuente de datos compatible y configurar PostgreSQL, Python y BigQuery.

La automatización semanal utiliza Windows Task Scheduler y depende del entorno local.

Por motivos de seguridad y tamaño, el repositorio no incluye los datos transaccionales originales ni el archivo .pbix. Las siete capturas permiten revisar visualmente el dashboard.

Es importante tener en cuenta que:

Los datos corresponden a 2009–2011 y no representan el comportamiento actual del mercado.

Diciembre de 2011 es un período incompleto.

El análisis no incluye toda la información necesaria para decidir compras o reposiciones, como márgenes e inventarios actuales.

BigQuery se utilizó mediante Sandbox.

Las alertas responden a reglas definidas y no a un modelo predictivo.

El proyecto no representa una implementación en producción.

Seguridad

La copia destinada a GitHub excluye credenciales, archivos .env con información sensible, datos transaccionales originales, logs y archivos locales de trabajo.

Incluye un .env.example como referencia para la configuración, sin contraseñas reales.

Los cambios futuros deben revisarse antes de publicarse, incluyendo los archivos y el historial de Git.

Qué me aportó este proyecto

Este trabajo me permitió integrar actividades que normalmente se presentan por separado: entender una necesidad de negocio, preparar la información, establecer reglas de cálculo, automatizar procesos y presentar resultados a través de indicadores.

También reforzó algo que considero importante en Business Intelligence: un dashboard no debería limitarse a mostrar cifras. Debe permitir entender qué representan, cómo se calcularon y qué preguntas vale la pena investigar a partir de ellas.

El proyecto reúne conocimientos de SQL, PostgreSQL, Python, BigQuery, Power BI, DAX, análisis funcional, calidad de datos y automatización de reportes, aplicados a un caso comercial de principio a fin.

Retail Analytics V18 — Proyecto de portafolio profesional

Business Intelligence · Data Analytics · SQL · Python · Power BI · Google BigQuery
