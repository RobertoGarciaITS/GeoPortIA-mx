# GeoPortIA Intelligence Map — mapa competitivo

**Estado:** análisis inicial para validar  
**Versión:** MVP-0.1  
**Fecha de revisión:** 2026-10-03

## 1. Resumen

GeoPortIA Intelligence Map se ubica entre cuatro categorías: inteligencia geoespacial, inteligencia laboral, desarrollo económico y workforce intelligence. La propuesta combina cartografía oficial mexicana, unidades económicas, contexto laboral y señales de demanda de habilidades.

No se identificó en esta revisión un producto idéntico que combine exactamente:

```text
INEGI + DENUE + ENOE + vacantes
+ mapa geoespacial
+ análisis de habilidades
+ déficit laboral
+ comparación de ciudades mexicanas
```

La competencia está fragmentada: unas plataformas son fuertes en inteligencia laboral, otras en location intelligence y otras en desarrollo económico.

## 2. Competidores prioritarios

| Prioridad | Producto | Clasificación | Motivo de comparación |
|---:|---|---|---|
| 1 | [Lightcast](https://lightcast.io/solutions/labor-market-intelligence) | Directo/proxy | Empleos, habilidades, salarios, oferta, demanda, talento regional y estrategia de localización. |
| 2 | [Chmura JobsEQ](https://www.chmura.com/) | Directo/proxy | Datos laborales y económicos, mapas, workforce planning, educación y site selection. |
| 3 | [GURU Site Selection](https://www.esri.com/partners/gis-webtech-a2T70000000TQIsEAO/guru-site-selection-a2d5x000002UKblAAG) | Directo en desarrollo económico | Workforce, infraestructura, transporte, servicios, incentivos y selección de sitios para gobiernos. |
| 4 | [Vista Site Selection](https://www.vistasiteselection.com/tools/) | Directo en site selection | Análisis laboral, salarios, talento, costos, infraestructura, riesgo y ubicación. |
| 5 | [DataMéxico](https://www.economia.gob.mx/datamexico/en) | Proxy público mexicano | Ciudades, industrias, ocupaciones, instituciones y perfiles regionales. |
| 6 | [ArcGIS Business Analyst](https://www.esri.com/en-us/arcgis/products/arcgis-business-analyst/overview) | Proxy geoespacial | Datos demográficos, empresariales, laborales, mercados y selección de ubicaciones. |
| 7 | [Metropolis IQ](https://www.metropolisiq.io/products/insights) | Proxy | Datos económicos y laborales para gobiernos, workforce development y localización. |
| 8 | [CARTO Site Selection](https://carto.com/solutions/site-selection/index.html) | Proxy geoespacial | Location intelligence, selección de sitios, áreas de mercado y datos espaciales. |
| 9 | [Targomo](https://www.targomo.com/) | Proxy geoespacial | Location intelligence, selección de sitios, redes, accesibilidad e isócronas. |
| 10 | [SiteIQ / GeoScope](https://www.geoscopanalytics.com/siteiq) | Proxy geoespacial | Scoring de oportunidades, restricciones, infraestructura y reportes de localización. |

## 3. Competidores directos o más cercanos

### Lightcast

Es el competidor más fuerte en inteligencia laboral. Su propuesta pública incluye datos sobre empleos, habilidades, salarios, oferta, demanda y talento por región, además de productos para empresas, educación y sector público.

Referencia: [Labor Market Intelligence — Lightcast](https://lightcast.io/solutions/labor-market-intelligence).

### Chmura JobsEQ

Es comparable por la combinación de datos laborales, económicos, mapas, reportes, educación, desarrollo económico y selección de sitios. También ofrece acceso mediante API, entrega en la nube o feeds personalizados.

Referencia: [JobsEQ — Chmura](https://www.chmura.com/).

### GURU Site Selection

Es un competidor relevante para el segmento de gobiernos y desarrollo económico. Integra datos GIS, workforce, infraestructura, transporte, servicios, incentivos y herramientas para responder solicitudes de información de inversión.

Referencia: [GURU Site Selection — Esri Partner Solution](https://www.esri.com/partners/gis-webtech-a2T70000000TQIsEAO/guru-site-selection-a2d5x000002UKblAAG).

### Vista Site Selection

Combina análisis laboral, datos ocupacionales, salarios, commute-shed, talento, costos, infraestructura y marcos de scoring para selección de mercados y sitios.

Referencia: [Vista tools](https://www.vistasiteselection.com/tools/).

## 4. Proxy públicos y mexicanos

### DataMéxico

Es el sustituto público mexicano más relevante. Permite explorar y comparar ciudades, industrias, ocupaciones, instituciones y perfiles, con visualizaciones y descarga de información.

Referencia: [DataMéxico](https://www.economia.gob.mx/datamexico/en).

### STPS — Estadísticas del Sector

La plataforma de la Secretaría del Trabajo integra y difunde información laboral sobre empleo, salarios, condiciones de trabajo, encuestas, registros administrativos y tableros.

Referencia: [STPS — Estadísticas del Sector](https://www.stps.gob.mx/gobmx/estadisticas/dgiet/index.html).

### Observatorio Laboral

Servicio público de información sobre carreras, ocupaciones y tendencias laborales por entidad federativa. Compite como fuente de consulta laboral, aunque no como plataforma de análisis geoespacial empresarial.

Referencia: [Observatorio Laboral](https://www.observatoriolaboral.gob.mx/).

### DENUE

El DENUE proporciona datos de identificación, ubicación, actividad económica y tamaño de establecimientos, además de API para consultas programáticas. Es una fuente complementaria y, en algunos casos, un sustituto parcial del componente empresarial de GeoPortIA.

Referencia: [API del DENUE](https://www.inegi.org.mx/servicios/api_denue.html).

## 5. Competidores geoespaciales

- [ArcGIS Business Analyst](https://www.esri.com/en-us/arcgis/products/arcgis-business-analyst/overview): inteligencia de mercados, datos demográficos, empresas, workforce y análisis de ubicación.
- [CARTO Site Selection](https://carto.com/solutions/site-selection/index.html): análisis de localización, áreas de mercado y más de 12,000 datasets espaciales declarados en su sitio.
- [Targomo](https://www.targomo.com/): location intelligence, redes, accesibilidad, isócronas y selección de sitios.
- [SiteIQ / GeoScope](https://www.geoscopanalytics.com/siteiq): screening, restricciones, scoring, infraestructura y reportes de oportunidad.
- [Metropolis IQ](https://www.metropolisiq.io/products/insights): análisis económico, workforce y site selection para gobiernos, consultores y empresas.

## 6. Sustitutos indirectos

Los usuarios también pueden resolver partes del problema con:

- QGIS y análisis manual.
- Excel o Google Sheets.
- Power BI o Tableau.
- Reportes PDF de gobierno o consultoras.
- Consultoría de desarrollo económico.
- Consultas independientes a INEGI, DENUE, ENOE y DataMéxico.
- Bolsas de trabajo y plataformas de perfiles profesionales.

Estos sustitutos son importantes porque el producto no solo compite contra software: también compite contra procesos manuales, hojas de cálculo y contratación de consultoría.

## 7. Matriz de comparación inicial

| Producto | Geoespacial | Laboral | Habilidades | Desarrollo económico | México | API/exportación |
|---|---:|---:|---:|---:|---:|---:|
| GeoPortIA | Alto, en construcción | Medio, en construcción | Medio, piloto AWS | Alto, objetivo | Alto, objetivo | Alto, objetivo |
| Lightcast | Medio/alto | Muy alto | Muy alto | Alto | Variable por cobertura | Alto |
| JobsEQ | Alto | Alto | Alto | Alto | Variable por cobertura | Alto |
| GURU | Muy alto | Alto | Medio/alto | Muy alto | Variable | Alto |
| Vista | Alto | Alto | Medio/alto | Muy alto | Bajo/variable | Medio |
| DataMéxico | Medio/alto | Medio/alto | Medio | Alto | Muy alto | Medio/alto |
| ArcGIS Business Analyst | Muy alto | Medio | Medio | Alto | Variable por dataset | Alto |
| CARTO | Muy alto | Variable | Variable | Medio/alto | Variable | Muy alto |

Las puntuaciones de GeoPortIA son objetivos del producto, no resultados ya demostrados. Las puntuaciones de terceros son una primera clasificación cualitativa basada en sus capacidades públicas y deben validarse con demos, documentación técnica y pruebas de cobertura.

## 8. Posicionamiento recomendado

La oportunidad más clara no es competir frontalmente con Lightcast o ArcGIS en cobertura global. Es especializarse en:

> Inteligencia geoespacial y laboral accesible para ciudades mexicanas, con fuentes públicas trazables y enfoque en brechas de habilidades, desarrollo económico y capacitación regional.

### Nichos iniciales

1. Inteligencia laboral municipal y estatal.
2. Diagnóstico de talento para parques industriales y clústeres.
3. Alineación universidad–empresa.
4. Planeación de capacitación regional.
5. Diagnóstico reproducible para agencias de desarrollo económico.

## 9. Próxima validación competitiva

Antes de afirmar diferenciación comercial se recomienda:

1. Solicitar demos de Lightcast, JobsEQ, GURU y Vista.
2. Verificar cobertura real para Coahuila, Nuevo León, Jalisco y Saltillo.
3. Comparar definición de oferta, demanda, habilidades y periodo.
4. Medir disponibilidad de APIs, precios y restricciones de uso.
5. Entrevistar a un usuario municipal, uno educativo y uno empresarial.
6. Comparar un mismo caso de uso: “escasez de programadores AWS en Saltillo”.

## 10. Fuentes consultadas

- [Lightcast — Labor Market Intelligence](https://lightcast.io/solutions/labor-market-intelligence)
- [Chmura — JobsEQ](https://www.chmura.com/)
- [GURU Site Selection — Esri](https://www.esri.com/partners/gis-webtech-a2T70000000TQIsEAO/guru-site-selection-a2d5x000002UKblAAG)
- [Vista Site Selection](https://www.vistasiteselection.com/tools/)
- [DataMéxico](https://www.economia.gob.mx/datamexico/en)
- [STPS — Estadísticas del Sector](https://www.stps.gob.mx/gobmx/estadisticas/dgiet/index.html)
- [Observatorio Laboral](https://www.observatoriolaboral.gob.mx/)
- [API del DENUE](https://www.inegi.org.mx/servicios/api_denue.html)
- [ArcGIS Business Analyst](https://www.esri.com/en-us/arcgis/products/arcgis-business-analyst/overview)
- [CARTO — Site Selection](https://carto.com/solutions/site-selection/index.html)
- [Targomo](https://www.targomo.com/)
- [SiteIQ / GeoScope](https://www.geoscopanalytics.com/siteiq)
- [Metropolis IQ](https://www.metropolisiq.io/products/insights)

