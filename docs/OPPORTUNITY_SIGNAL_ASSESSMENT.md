# GeoPortIA Intelligence Map — evaluación de señal de oportunidad

**Estado:** investigación inicial y diseño de validación  
**Fecha:** 2026-10-03  
**Contrato relacionado:** `GEOOPPORTUNITY-INTELLIGENCE-MAP-MVP-001`

## 1. Conclusión ejecutiva

La señal de oportunidad para una solución de inteligencia geoespacial y laboral en México es **fuerte como problema**, **media como diferenciación** y **no validada todavía como negocio**.

La evidencia externa apunta a una combinación relevante:

```text
desajuste de habilidades
+ demanda de talento digital
+ nearshoring y desarrollo regional
+ necesidad de información laboral local
+ uso creciente de datos geoespaciales para decidir
```

Esto no demuestra por sí solo disposición de pago ni adopción. La oportunidad debe validarse con un caso de uso real y usuarios concretos.

## 2. Evidencia de la señal

### Desajuste regional de habilidades

La OCDE reporta que 36% de los trabajadores en México están en empleos que no corresponden con su nivel educativo. La proporción varía entre regiones, aproximadamente de 23% a 44%, lo que indica que el problema tiene una dimensión territorial y no solamente nacional.

Fuente: [OECD — Mexico country note, Job Creation and Local Economic Development 2024](https://www.oecd-ilibrary.org/en/publications/job-creation-and-local-economic-development-2024-country-notes_ad2806c1-en/mexico_0e0d74d9-en.html).

### Escasez de talento digital

El BID describe una brecha creciente en manufactura avanzada y tecnologías digitales en México, incluyendo cloud computing, ciberseguridad, inteligencia artificial y datos. También reporta que 68% de los empleadores tienen dificultad para encontrar talento calificado.

Fuente: [BID — Closing the Digital Talent Gap](https://www.iadb.org/en/blog/labor-markets/closing-digital-talent-gap-model-driving-mexicos-productive-future).

### Demanda de habilidades en América Latina

El BID señala que la demanda de habilidades digitales y tecnológicas en vacantes de América Latina aumentó de 16% a 19% en un periodo reciente y que las empresas buscan combinaciones de habilidades, no solamente credenciales académicas.

Fuente: [BID — How Can We Develop the Skills for Tomorrow’s Jobs?](https://www.iadb.org/en/blog/labor-markets/how-can-we-develop-skills-tomorrows-jobs).

### Nearshoring y desarrollo regional

El Banco de México, la CEPAL y organismos multilaterales están estudiando el efecto del nearshoring, la manufactura avanzada y la disponibilidad de talento sobre las regiones mexicanas.

Fuentes:

- [Banco de México — Early effects of nearshoring in the manufacturing labor market](https://www.banxico.org.mx/DIBM/web/documento/visor.html?clave=2025-16&locale=en).
- [CEPAL — Nearshoring en México](https://www.cepal.org/es/notas/estudio-la-cepal-examina-nearshoring-mexico-sus-diversas-opciones-escalamiento-industrial).

### Información laboral municipal

INEGI cuenta con los Indicadores Laborales para los Municipios de México, lo que confirma la relevancia institucional de producir información laboral subnacional.

Fuente: [INEGI — Indicadores Laborales para los Municipios de México](https://www.inegi.org.mx/programas/ilmm/).

### Integración geoespacial para decisiones

La OCDE y el Banco Mundial señalan que la integración de datos estadísticos, geográficos y administrativos permite mejorar decisiones regionales, orientar presupuestos y diseñar servicios más focalizados.

Fuentes:

- [OECD — Using private sector geospatial data to inform policy](https://www.oecd.org/content/dam/oecd/en/publications/reports/2022/11/using-private-sector-geospatial-data-to-inform-policy_738fb3c8/242f51b8-en.pdf).
- [World Bank — Geospatial data for development operations](https://documents1.worldbank.org/curated/en/099422502202611616/pdf/IDU-a3bcd5b5-c863-4c21-ab90-0f7918012892.pdf).

## 3. Evaluación de fuerza de la señal

| Dimensión | Evaluación | Interpretación |
|---|---|---|
| Problema de desajuste | Fuerte | Hay evidencia regional y nacional. |
| Demanda de skills digitales | Fuerte | Cloud, datos, IA y ciberseguridad aparecen como áreas críticas. |
| Necesidad de análisis subnacional | Fuerte | La variación regional justifica comparar municipios y ciudades. |
| Utilidad de la geografía | Fuerte | La localización permite conectar empresas, talento e infraestructura. |
| Diferenciación de GeoPortIA | Media | Debe demostrar una experiencia mejor integrada para México. |
| Datos disponibles | Media | Existen fuentes, pero tienen diferentes periodos, coberturas y definiciones. |
| Disposición de pago | Desconocida | Requiere entrevistas y piloto con usuarios reales. |
| Competencia | Alta | Existen soluciones laborales, GIS y de desarrollo económico. |

## 4. Nicho recomendado

### Workforce Intelligence regional para México

GeoPortIA debe comenzar como una solución para:

- gobiernos municipales y estatales;
- universidades y centros de capacitación;
- clústeres industriales;
- parques industriales;
- empresas que analizan expansión o contratación regional.

### Mensaje de posicionamiento

> GeoPortIA conecta empresas, habilidades, vacantes y territorio para identificar oportunidades y brechas de talento en las ciudades mexicanas.

## 5. Primer piloto verificable

### Pregunta

> ¿Dónde existe una posible brecha de talento digital relacionada con nearshoring en el corredor Coahuila–Nuevo León?

### Geografías

1. Saltillo.
2. Ramos Arizpe.
3. Monterrey.

### Habilidades iniciales

- AWS/cloud.
- Datos y analítica.
- Ciberseguridad.
- Automatización industrial.

### Capas

```text
Empresas por actividad económica
Oferta laboral disponible y ocupada
Vacantes observadas
Instituciones educativas o de capacitación
Infraestructura industrial disponible
Periodo y calidad del dato
```

### Salida del piloto

- mapa por ciudad y actividad;
- tabla de oferta y demanda;
- déficit absoluto;
- índice relativo;
- empresas relacionadas;
- fuentes y periodos;
- advertencias metodológicas;
- exportación JSON/CSV/GeoJSON;
- una recomendación de siguiente acción, no una decisión automática.

## 6. Lo que el piloto debe demostrar

| Pregunta | Criterio de éxito |
|---|---|
| ¿El usuario entiende el mapa? | Puede explicar la diferencia entre tres ciudades. |
| ¿El indicador es auditable? | Puede ver fuente, periodo y fórmula. |
| ¿La comparación es útil? | Identifica una ciudad o habilidad para investigar. |
| ¿Los datos son comparables? | Se documentan cobertura y limitaciones. |
| ¿Genera una acción? | Propone capacitación, contratación, investigación o inversión. |
| ¿Se reutiliza el modelo? | El mismo contrato funciona para otra habilidad. |

## 7. Riesgos de interpretación

- ENOE no es un inventario directo de personas que dominen AWS.
- DENUE muestra establecimientos, no necesariamente vacantes.
- Vacantes publicadas no representan toda la demanda del mercado.
- El déficit depende de la definición de oferta y demanda.
- Las ciudades pueden tener distinta cobertura estadística.
- La relación entre demanda y oportunidad no es causal.
- Un índice alto no garantiza una oportunidad comercial.

Por eso el producto debe usar lenguaje como **señal**, **proxy**, **posible brecha** y **requiere validación**.

## 8. Próximas pruebas de mercado

1. Entrevistar a un responsable de desarrollo económico.
2. Entrevistar a un responsable de capacitación o universidad.
3. Entrevistar a un reclutador o empresa industrial.
4. Ejecutar la misma consulta con fuentes reales.
5. Comparar el resultado con DataMéxico, STPS y proveedores privados.
6. Medir tiempo para obtener una conclusión con y sin GeoPortIA.
7. Preguntar qué formato se compraría: dashboard, informe, API o servicio analítico.

## 9. Criterio de decisión

Después del piloto, elegir una dirección principal:

```text
A. Workforce Intelligence regional
B. Economic Development Intelligence
C. Location Intelligence para expansión
D. Public Asset Intelligence
```

La opción recomendada para el siguiente ciclo es **A: Workforce Intelligence regional**, porque es la que mejor conecta el código actual, la evidencia de desajuste laboral y el interés en habilidades digitales.

## 10. Nota metodológica

Las cifras y conclusiones externas se utilizan para evaluar la existencia del problema, no para afirmar que GeoPortIA ya lo resuelve. El repositorio mantiene sus escenarios laborales actuales como `synthetic` o `controlled` hasta ejecutar una integración real documentada.

