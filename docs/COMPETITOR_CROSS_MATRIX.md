# GeoPortIA Intelligence Map — matriz cruzada de competidores

**Estado:** análisis comparativo inicial  
**Fecha:** 2026-10-04  
**Contrato relacionado:** `GEOOPPORTUNITY-INTELLIGENCE-MAP-MVP-001`

## 1. Cómo leer la matriz

La tabla compara capacidades públicas observables, no calidad interna ni participación de mercado. Las marcas se clasifican así:

- **Alta:** es una capacidad central y visible del producto.
- **Media:** existe como capacidad parcial, complemento o depende de datos/licencias.
- **Baja:** no es el foco principal o requiere integración externa.
- **GeoPortIA objetivo:** capacidad que el MVP busca demostrar, no una afirmación de que ya esté completa en producción.

## 2. Matriz cruzada

| Producto / solución | Tipo | Mapa analítico | Empresas / actividad | Workforce / empleo | Skills | Oferta-demanda | México público | Comparación ciudad | API / exportación | Trazabilidad | Activos públicos | Propuesta principal |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **GeoPortIA Intelligence Map** | Producto en construcción | Alta | Alta | Media | Media | Media | Alta | Alta | Alta | Alta, objetivo | Media, futuro | Conectar territorio, empresas, talento y demanda con fuentes trazables |
| [DataMéxico](https://www.economia.gob.mx/datamexico/en) | Sustituto público mexicano | Media | Media | Media/alta | Media | Baja/media | Muy alta | Alta | Media | Alta | Baja | Explorar perfiles económicos, ciudades, industrias y ocupaciones |
| [INEGI DENUE](https://www.inegi.org.mx/servicios/api_denue.html) | Fuente / sustituto parcial | Media | Muy alta | Baja | Baja | Baja | Muy alta | Media | Alta | Muy alta | Baja | Consultar unidades económicas, actividad y ubicación |
| [INEGI ILMM](https://www.inegi.org.mx/programas/ilmm/) | Indicador público | Baja/media | Baja | Media/alta | Baja | Baja | Muy alta | Alta | Media | Muy alta | Baja | Producir indicadores laborales municipales |
| [STPS Estadísticas](https://www.stps.gob.mx/gobmx/estadisticas/dgiet/index.html) | Portal público laboral | Baja | Baja | Alta | Media | Baja/media | Muy alta | Media | Baja/media | Alta | Baja | Consultar estadísticas laborales y tableros públicos |
| [Observatorio Laboral](https://www.observatoriolaboral.gob.mx/) | Portal público laboral | Baja | Baja | Media | Media | Baja | Muy alta | Media | Baja | Media/alta | Baja | Orientar carreras y ocupaciones por entidad |
| [Lightcast](https://lightcast.io/solutions/labor-market-intelligence) | Competidor directo/proxy | Media/alta | Media | Muy alta | Muy alta | Alta | Variable | Alta | Alta | Alta, propietaria | Baja/media | Labor market intelligence, skills, salarios y talento regional |
| [Chmura JobsEQ](https://www.chmura.com/) | Competidor directo/proxy | Alta | Media | Alta | Alta | Media/alta | Variable | Alta | Alta | Alta, propietaria | Baja/media | Labor intelligence, economía regional, mapas y reportes |
| [ArcGIS Business Analyst](https://www.esri.com/en-us/arcgis/products/arcgis-business-analyst/overview) | Competidor proxy geoespacial | Muy alta | Alta | Media | Baja/media | Baja/media | Variable | Muy alta | Alta | Alta, depende de datasets | Media | Market intelligence, demografía y selección de ubicaciones |
| [GURU Site Selection](https://www.esri.com/partners/gis-webtech-a2T70000000TQIsEAO/guru-site-selection-a2d5x000002UKblAAG) | Competidor proxy desarrollo económico | Muy alta | Alta | Alta | Media | Media | Variable | Muy alta | Alta | Alta, configurable | Media | Selección de sitios, workforce, infraestructura e incentivos |
| [Vista Site Selection](https://www.vistasiteselection.com/tools/) | Competidor proxy desarrollo económico | Alta | Media | Alta | Media/alta | Media | Variable | Alta | Media | Alta, propietaria | Baja/media | Site selection, labor analytics y marcos de scoring |
| [CARTO Site Selection](https://carto.com/solutions/site-selection/index.html) | Competidor proxy geoespacial | Muy alta | Alta | Variable | Variable | Baja/media | Variable | Muy alta | Muy alta | Alta, depende de datasets | Media | Location intelligence y análisis espacial empresarial |
| [Targomo](https://www.targomo.com/) | Competidor proxy geoespacial | Muy alta | Alta | Baja/media | Baja | Baja | Variable | Muy alta | Muy alta | Alta, depende de datasets | Media | Accesibilidad, redes, isócronas y expansión |

## 3. Lectura por dimensión

### Geografía

ArcGIS Business Analyst, CARTO, Targomo y las soluciones de site selection tienen mayor profundidad geoespacial que el MVP actual. GeoPortIA no debe competir inicialmente por cantidad de herramientas GIS, sino por el significado de las capas mexicanas y la decisión que ayudan a tomar.

### Inteligencia laboral

Lightcast y JobsEQ son los referentes más fuertes en datos laborales, skills, salarios, demanda y workforce analytics. GeoPortIA debe evitar competir de inicio por cobertura global y concentrarse en integración local, transparencia y casos de ciudad.

### Información pública mexicana

DataMéxico, INEGI, STPS y OLA ofrecen piezas importantes del problema. La oportunidad de GeoPortIA está en integrar esas piezas con una experiencia de decisión común, no en sustituir las fuentes oficiales.

### Desarrollo económico

GURU, Vista y Metropolis IQ —investigado en el mapa competitivo general— son referentes para selección de sitios, workforce y atracción de inversión. GeoPortIA puede diferenciarse con una entrada más ligera, enfocada inicialmente en México y en fuentes públicas trazables.

### Activos públicos

La mayoría de las soluciones laborales y de site selection no tiene como foco principal la operación de activos públicos municipales. Esta dimensión puede ser una expansión transversal posterior, por ejemplo para luminarias, semáforos, parques o infraestructura urbana.

## 4. Razón de la propuesta de valor

La propuesta de valor no se basa en que no existan mapas o plataformas de workforce intelligence. Se basa en la combinación de cinco elementos:

```text
Fuentes públicas mexicanas
+ geografía municipal
+ empresas y actividades económicas
+ habilidades y vacantes
+ explicación de fuentes y fórmulas
```

### 4.1 Integración de fuentes fragmentadas

El usuario normalmente debe consultar por separado:

- DENUE para empresas.
- ENOE o ILMM para contexto laboral.
- DataMéxico para perfiles económicos y ocupacionales.
- STPS/OLA para información laboral.
- Fuentes de vacantes para demanda.
- QGIS, Excel o BI para cruzar los resultados.

GeoPortIA busca convertir ese proceso en una consulta territorial única y exportable.

### 4.2 Enfoque municipal y regional

El MVP parte de Saltillo y compara ciudades bajo la misma definición. Esto habilita una conversación concreta sobre:

- capacitación;
- expansión empresarial;
- desarrollo económico;
- disponibilidad de talento;
- brechas de habilidades.

### 4.3 Trazabilidad

Cada indicador debe mostrar:

```text
fuente
periodo
versión
estado del dato
fórmula
limitaciones
```

Esto permite distinguir un dato oficial de un proxy, fixture o estimación.

### 4.4 Interoperabilidad

La salida en API, JSON, CSV y GeoJSON permite continuar el análisis en QGIS, Excel, Power BI u otros sistemas. La plataforma no obliga al usuario a permanecer en una sola interfaz.

### 4.5 Transversalidad futura

El núcleo puede reutilizarse para otros verticales:

```text
Labor Intelligence
Economic Development Intelligence
Business Intelligence
Public Asset Intelligence
Urban Operations
```

La transversalidad es una capacidad de arquitectura, no una razón para ampliar el MVP sin validación.

## 5. Competidores por tipo

### Directos o más cercanos

- Lightcast.
- Chmura JobsEQ.
- GURU Site Selection.
- Vista Site Selection.
- Metropolis IQ.

### Proxies geoespaciales

- ArcGIS Business Analyst.
- CARTO.
- Targomo.
- SiteIQ/GeoScope.

### Sustitutos públicos mexicanos

- DataMéxico.
- INEGI DENUE.
- INEGI ILMM.
- STPS Estadísticas.
- Observatorio Laboral.

### Sustitutos manuales

- QGIS.
- Excel o Google Sheets.
- Power BI o Tableau.
- Consultoría y reportes PDF.

## 6. Posición recomendada

GeoPortIA debe posicionarse como:

> Workforce and Economic Development Intelligence Map para ciudades mexicanas.

Mensaje corto:

> Conecta empresas, habilidades, vacantes y territorio para revelar oportunidades regionales.

No debe posicionarse todavía como:

- plataforma nacional completa;
- predictor de empleo;
- sistema oficial de estadísticas;
- sustituto de INEGI;
- sistema de decisión automática;
- competidor global de ArcGIS o Lightcast.

## 7. Caso de comparación recomendado

La matriz debe probarse con una misma pregunta en:

```text
Saltillo
Ramos Arizpe
Monterrey
```

Pregunta:

> ¿Dónde existe una posible brecha de talento digital relacionada con manufactura avanzada y nearshoring?

Habilidades piloto:

- AWS/cloud.
- datos y analítica.
- ciberseguridad.
- automatización industrial.

El resultado debe incluir valores, fuentes, periodo, cobertura y advertencias, no solamente un color o ranking.

## 8. Conclusión

GeoPortIA tiene una propuesta de valor potencial porque puede ocupar la capa de integración y decisión entre fuentes públicas mexicanas, plataformas laborales y herramientas GIS. La ventaja todavía es una hipótesis y debe demostrarse con:

1. un caso real;
2. una comparación reproducible;
3. usuarios que tomen una decisión;
4. datos con fuentes y periodos defendibles;
5. un resultado mejor que la suma de consultas manuales.

