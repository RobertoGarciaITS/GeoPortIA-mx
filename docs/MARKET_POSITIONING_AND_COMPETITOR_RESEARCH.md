# GeoPortIA Intelligence Map
## Funciones, propuesta de valor y análisis competitivo

**Estado:** hipótesis de posicionamiento para validar  
**Versión:** MVP-0.1  
**Categoría inicial:** intelligence map / location intelligence / workforce intelligence

## 1. Qué es el producto

GeoPortIA Intelligence Map es una plataforma de inteligencia territorial que relaciona geografía, actividad económica y mercado laboral. Su propósito es ayudar a identificar oportunidades y brechas regionales mediante mapas, indicadores, filtros y comparaciones entre ciudades.

```text
Territorio + Empresas + Talento + Demanda laboral
                          ↓
              Inteligencia para decisiones regionales
```

## 2. Tabla de funciones

| Función | Qué hace | Usuario principal | Resultado |
|---|---|---|---|
| Mapa territorial | Muestra municipios, ciudades, áreas urbanas, manzanas, vialidades y límites | Analista territorial | Comprensión espacial |
| Capa empresarial | Ubica y clasifica unidades económicas del DENUE | Desarrollo económico | Concentración sectorial |
| Capa de talento | Integra señales de oferta laboral y perfiles disponibles | Talento y capacitación | Oferta potencial |
| Capa de demanda | Integra vacantes y habilidades solicitadas | Empresas y analistas | Demanda observable |
| Indicador de brecha | Calcula oferta, demanda, déficit e índice de escasez | Planeación | Priorización de oportunidades |
| Comparación de ciudades | Compara ciudades con la misma habilidad y periodo | Dirección/planeación | Benchmark territorial |
| Filtros | Filtra país, estado, ciudad, habilidad y métrica | Todos | Exploración dirigida |
| Tabla auditable | Muestra valores, fuente, periodo y estado del dato | Analista | Trazabilidad |
| Exportación | Genera JSON, CSV y GeoJSON | Analista técnico | Reutilización en QGIS, Excel o BI |
| Integración QGIS | Permite validar cartografía y exportar mapas | GIS | Control geográfico |
| API | Sirve datos normalizados al frontend y otros clientes | Desarrollo | Escalabilidad |
| QA de datos | Ejecuta pruebas, smoke tests y validación de contratos | Equipo técnico | Confianza operativa |

## 3. Propuesta de valor

### Propuesta principal

> GeoPortIA convierte datos geográficos, empresariales y laborales dispersos en una vista territorial accionable para detectar dónde existe concentración económica, demanda de habilidades y posibles brechas de talento.

### Valor por tipo de usuario

| Usuario | Problema | Valor que entrega GeoPortIA |
|---|---|---|
| Gobierno municipal/estatal | Datos separados y difícil comparación regional | Identificación de sectores, zonas y habilidades prioritarias |
| Desarrollo económico | Falta de evidencia para atraer inversión | Perfil territorial con empresas, infraestructura y talento |
| Universidades | Programas formativos desconectados del mercado | Señales para alinear capacitación con demanda observable |
| Empresas | Dificultad para evaluar disponibilidad regional | Comparación de talento y presión de contratación |
| Consultoría | Mucho tiempo integrando fuentes | Flujo reproducible con API, mapas y exportaciones |
| Analista GIS | Datos laborales fuera del mapa | Cruce entre geometría, actividad económica e indicadores |

## 4. Diferenciadores propuestos

Estos son diferenciadores hipotéticos del MVP; deben validarse contra productos existentes.

| Diferenciador | Explicación | Evidencia que debe construirse |
|---|---|---|
| Enfoque geográfico-laboral integrado | No muestra solamente mapas ni solamente vacantes; relaciona territorio y talento | Caso reproducible de Saltillo |
| Orientación a ciudades mexicanas | Prioriza fuentes y claves geográficas de México | Integración INEGI/DENUE/ENOE |
| Trazabilidad de indicadores | Cada valor conserva fuente, periodo, versión y estado | Contrato de datos y tabla auditable |
| Comparación normalizada | Compara ciudades bajo la misma habilidad y definición | Benchmark Saltillo–Monterrey–Guadalajara |
| Interoperabilidad GIS | Exporta GeoJSON/CSV y se conecta con QGIS | Flujos de exportación validados |
| Construcción abierta y reproducible | El pipeline puede ejecutarse localmente, en Codespaces y GCP | Tests y despliegue repetible |
| Proxy de oportunidad | Puede señalar una oportunidad sin presentarla como predicción | Metodología documentada y etiquetas de incertidumbre |

## 5. Categoría e industria

### Categoría primaria

**Location Intelligence / Geospatial Business Intelligence**

### Categorías secundarias

- Workforce Intelligence.
- Labor Market Intelligence.
- Economic Development Intelligence.
- Talent Location Analytics.
- GIS Decision Support.
- Regional Competitiveness Analytics.
- Smart City / Urban Intelligence.

### Industria o grupo de servicios

GeoPortIA podría posicionarse como una solución B2G/B2B2G de software y analítica para:

- Gobiernos locales y estatales.
- Agencias de desarrollo económico.
- Instituciones educativas y de capacitación.
- Empresas de consultoría territorial y laboral.
- Empresas que evalúan expansión regional.
- Parques industriales y clústeres sectoriales.

La categoría más precisa para el MVP es:

> Plataforma de inteligencia geoespacial para análisis de talento, empresas y oportunidades regionales.

## 6. Competidores directos, proxy e indirectos

### Competidor directo

Producto que combina mapa territorial, empresas, oferta/demanda laboral e indicadores de brecha para apoyar decisiones regionales.

### Competidor proxy

Producto que resuelve una parte sustancial del mismo problema, aunque no combine todas las capas. Ejemplos de grupos a investigar:

- Plataformas de location intelligence.
- Plataformas de workforce analytics.
- Marketplaces o agregadores de vacantes con analítica geográfica.
- Plataformas de economic development analytics.
- Herramientas de site selection.
- Proveedores de datos geográficos y empresariales.

### Competidor indirecto o sustituto

Forma alternativa de resolver el problema:

- Excel y hojas de cálculo.
- QGIS y análisis manual.
- Power BI/Tableau con datos integrados por consultoría.
- Reportes PDF de gobierno o consultoras.
- Consultoría especializada sin plataforma continua.
- Consultas independientes a INEGI, DENUE y bolsas de empleo.

## 7. Matriz para evaluar competidores

| Criterio | Pregunta | Escala sugerida |
|---|---|---|
| Cobertura geográfica | ¿Opera en México y a qué nivel territorial? | 0–5 |
| Datos empresariales | ¿Incluye empresas y actividad económica? | 0–5 |
| Datos laborales | ¿Incluye oferta, demanda o vacantes? | 0–5 |
| Habilidades | ¿Permite comparar skills específicas? | 0–5 |
| Componente geoespacial | ¿El mapa es analítico o solo decorativo? | 0–5 |
| Brecha laboral | ¿Calcula déficit o escasez? | 0–5 |
| Trazabilidad | ¿Expone fuente, periodo y metodología? | 0–5 |
| Interoperabilidad | ¿Tiene API, CSV, GeoJSON o conectores? | 0–5 |
| Actualización | ¿Con qué frecuencia actualiza datos? | 0–5 |
| Segmento | ¿Sirve a gobierno, empresas, educación o todos? | 0–5 |
| Precio/acceso | ¿Es público, SaaS, consultoría o enterprise? | 0–5 |
| Diferenciación | ¿Qué problema resuelve mejor que GeoPortIA? | Texto |

## 8. Prompt para investigación de competidores

Copiar y pegar el siguiente prompt en una herramienta de investigación web o análisis competitivo:

```text
Actúa como analista senior de estrategia, inteligencia de mercado y geospatial business intelligence.

Investiga el mercado de plataformas que combinan mapas, datos geográficos, empresas, talento, vacantes y análisis de oportunidades regionales.

Producto a analizar:
GeoPortIA Intelligence Map, una plataforma en construcción que integra cartografía de INEGI, unidades económicas del DENUE, contexto laboral de ENOE y señales de demanda de habilidades para comparar ciudades y detectar posibles brechas territoriales de talento.

Objetivo de la investigación:
1. Identificar competidores directos.
2. Identificar competidores proxy que resuelvan una parte importante del problema.
3. Identificar sustitutos indirectos como QGIS, Excel, Power BI, reportes y consultoría.
4. Determinar la categoría de mercado más adecuada para el producto.
5. Encontrar nichos con baja cobertura o poca especialización.
6. Evaluar si la propuesta debe orientarse a gobierno, desarrollo económico, educación, empresas o consultoría.

Clasifica cada resultado como:
- Competidor directo.
- Competidor proxy.
- Sustituto indirecto.
- Proveedor de datos o infraestructura complementaria.

Para cada organización o producto entrega:
- Nombre.
- País y cobertura geográfica.
- Sitio web oficial.
- Tipo de cliente.
- Categoría de producto.
- Funciones principales.
- Capas de datos disponibles.
- Si integra mapas analíticos.
- Si mide oferta, demanda o brecha laboral.
- Si permite consultar habilidades específicas.
- API, exportación o interoperabilidad.
- Modelo comercial o precio publicado.
- Evidencia y fecha de consulta.
- Fortalezas frente a GeoPortIA.
- Debilidades o espacios donde GeoPortIA podría diferenciarse.

Evalúa cada producto de 0 a 5 en:
- Inteligencia geoespacial.
- Inteligencia laboral.
- Datos empresariales.
- Análisis de habilidades.
- Comparación entre ciudades.
- Trazabilidad de fuentes.
- Actualización de datos.
- API/interoperabilidad.
- Orientación a México.
- Utilidad para desarrollo económico.

Después genera:
1. Tabla comparativa.
2. Mapa de posicionamiento con ejes “profundidad geoespacial” y “profundidad laboral”.
3. Lista de competidores prioritarios para analizar.
4. Tres nichos posibles para GeoPortIA.
5. Tres propuestas de posicionamiento.
6. Riesgos de entrar al mercado.
7. Recomendación de segmento inicial.

No inventes funciones, clientes, precios ni cobertura. Distingue claramente entre hechos verificados, inferencias y supuestos. Usa fuentes primarias, enlaces directos y fecha de consulta. Prioriza resultados relevantes para México y América Latina, pero incluye referencias globales cuando sean comparables.
```

## 9. Hipótesis de nichos iniciales

1. **Inteligencia laboral municipal:** herramienta accesible para gobiernos que necesitan justificar capacitación y desarrollo económico.
2. **Talento para parques industriales y clústeres:** cruce de empresas, habilidades e infraestructura alrededor de una zona económica.
3. **Planeación universidad–empresa:** identificar diferencias entre programas educativos y demanda local de habilidades.
4. **Diagnóstico regional reproducible:** alternativa técnica a reportes manuales con fuentes trazables y exportación GIS.

Estas hipótesis no son conclusiones de mercado. Requieren entrevistas, análisis de competidores, pruebas con usuarios y validación de disposición de pago.

## 10. Siguiente validación

La siguiente actividad recomendada es ejecutar el prompt con una muestra de 15–20 productos y llenar la matriz competitiva. Después se debe entrevistar a tres perfiles: un usuario de gobierno/desarrollo económico, un responsable de talento y un analista GIS. El objetivo será verificar qué función tiene mayor valor antes de ampliar el producto.

