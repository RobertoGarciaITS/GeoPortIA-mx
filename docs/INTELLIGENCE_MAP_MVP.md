# GeoPortIA Intelligence Map — diseño y alcance del MVP

**Estado:** fase de construcción  
**Versión:** MVP-0.1  
**Repositorio:** `GeoPortIA-mx`

## 1. Contexto

GeoPortIA Intelligence Map es un tablero geoespacial para explorar la relación entre territorio, actividad económica y mercado laboral. El producto combina cartografía oficial, unidades económicas y señales de oferta/demanda de talento para ayudar a responder preguntas concretas sobre una ciudad:

> ¿Dónde están las empresas, qué capacidades laborales existen, qué puestos se solicitan y dónde aparece una posible brecha?

El MVP se construye primero con Saltillo como caso de referencia y con una comparación controlada contra Monterrey y Guadalajara. Los valores actuales del escenario laboral son sintéticos: sirven para validar el flujo, el contrato de datos, los filtros, los gráficos y las pruebas; no deben interpretarse como una medición oficial.

## 2. Objetivo del MVP

Entregar una primera versión reproducible que permita:

1. Seleccionar país, estado, ciudad, habilidad y métrica.
2. Visualizar las ciudades sobre un mapa y comparar sus indicadores.
3. Consultar una tabla Estado–Ciudad con oferta, demanda, déficit e índice.
4. Explicar el origen, periodo, cobertura y calidad de cada dato.
5. Sustituir posteriormente los fixtures por adaptadores oficiales sin rediseñar el frontend.

El MVP no pretende automatizar decisiones de contratación, inversión o política pública. Su función inicial es convertir datos heterogéneos en una vista espacial comprensible y auditable.

## 3. Usuario y decisiones soportadas

### Usuarios iniciales

- Analista territorial o de mercado laboral.
- Equipo de desarrollo económico municipal o estatal.
- Responsable de planeación de talento y capacitación.
- Equipo técnico que valida fuentes, consultas y calidad de datos.

### Decisiones soportadas

- Comparar presión relativa de una habilidad entre ciudades.
- Identificar ciudades que requieren una revisión más detallada.
- Ubicar la concentración de empresas de una actividad.
- Priorizar la siguiente consulta o carga de datos.

### Decisiones fuera del MVP

- Declarar una escasez laboral real sin validación estadística.
- Recomendar candidatos o empresas específicas.
- Predecir empleo futuro.
- Emitir una clasificación automática de ciudades para inversión.

## 4. Alcance funcional

### Incluido en MVP-0.1

| Módulo | Resultado esperado |
|---|---|
| Mapa | Límites municipales o urbanos y marcadores/áreas disponibles para el escenario seleccionado. |
| Filtros | País, estado, ciudad, habilidad y métrica. Países iniciales: México, Canadá y Estados Unidos. |
| Indicadores | Oferta disponible, demanda, déficit e índice de escasez. |
| Comparación | Vista conjunta de Saltillo, Monterrey y Guadalajara. |
| Tabla | Estado, ciudad, oferta, demanda, déficit, índice y fuente/periodo. |
| Gráficos | Comparación de demanda vs. oferta y ranking por índice. |
| Exportación | JSON y CSV para inspección, QGIS, Excel o Power BI. |
| API | Contratos locales preparados para conectar adaptadores INEGI/DENUE, ENOE y vacantes. |
| QA | Unit tests, smoke tests, validación de contrato y prueba de generación del dashboard. |

### Fuera de alcance de MVP-0.1

- Cobertura nacional operativa con actualización automática.
- Ingesta productiva programada y catálogo de habilidades completo.
- Autenticación, usuarios, roles, pagos y multi-tenant.
- IA generativa, scoring propietario o recomendaciones automáticas.
- Google Places/Routes como fuente analítica.
- Streaming, Redis, Kubernetes/GKE y arquitectura de microservicios.
- Sustituir la validación estadística oficial de ENOE por conteos simples.

## 5. Definición de indicadores

Para una ciudad `c`, habilidad `s` y periodo `t`:

```text
oferta = personas o perfiles disponibles identificados
demanda = vacantes o puestos solicitados
déficit = demanda - oferta
índice_de_escasez = demanda / oferta, si oferta > 0
```

Interpretación inicial:

- `índice > 1`: la demanda supera la oferta observada.
- `índice = 1`: equilibrio aproximado.
- `índice < 1`: la oferta observada supera la demanda.

Estos indicadores son señales exploratorias. La versión oficial deberá documentar deduplicación, fecha de corte, población objetivo, expansión muestral de ENOE, cobertura geográfica, definición de habilidad y margen de error cuando corresponda.

## 6. Fuentes y contrato de datos

### Fuentes previstas

- **INEGI Marco Geoestadístico:** límites, localidades, áreas urbanas, manzanas y vialidades.
- **DENUE:** unidades económicas, actividad, ubicación y atributos disponibles.
- **ENOE:** población ocupada, características laborales y variables de contexto; no equivale por sí sola a una bolsa de talento por habilidad.
- **SNE u otra fuente autorizada de vacantes:** demanda observable de puestos.

### Arquitectura de datos

```text
Fuentes oficiales / fixtures
        ↓
Adaptadores y normalización
        ↓
Contrato labor_indicators_v1
        ↓
API / almacenamiento futuro
        ↓
Dashboard Intelligence Map
```

La fuente de verdad no será el HTML generado. En construcción se usa `data/sample/labor_indicators_v1.json`; el esquema lógico futuro está en `sql/labor_indicators_schema.sql`. El dashboard genera HTML, JSON, CSV y GeoJSON como artefactos derivados.

Campos mínimos del indicador:

```text
country_code, state_code, state_name, city_code, city_name,
skill_code, skill_name, period, supply, demand, deficit,
scarcity_index, geometry_ref, source, source_version, data_status
```

`data_status` debe distinguir como mínimo `synthetic`, `official`, `estimated` y `stale`.

## 7. Diseño de experiencia

### Layout propuesto

```text
┌─────────────────────────────────────────────────────────────┐
│ Título, periodo, estado de datos y última actualización      │
├───────────────────────┬─────────────────────────────────────┤
│ Filtros               │ Mapa                               │
│ país                  │ ciudades / capas territoriales     │
│ estado                │ leyenda                             │
│ ciudad                │                                     │
│ habilidad             │                                     │
│ métrica               │                                     │
├───────────────────────┴─────────────────────────────────────┤
│ Tarjetas: oferta | demanda | déficit | índice                │
├─────────────────────────────────────────────────────────────┤
│ Gráfico comparativo y tabla Estado–Ciudad                    │
└─────────────────────────────────────────────────────────────┘
```

### Comportamiento

- Cambiar un filtro actualiza mapa, tarjetas, gráfico y tabla con el mismo conjunto de datos.
- Una ciudad seleccionada debe resaltarse y mostrar su estado, fuente y periodo.
- Si no hay datos para un país o combinación, se muestra “sin datos” y no cero.
- Los datos sintéticos deben mostrar una etiqueta visible de demostración.
- La tabla debe conservar una vista accesible aunque el mapa no cargue.

## 8. Diseño técnico del MVP

### Capas

1. **Datos:** fixtures versionados y archivos oficiales descargados.
2. **Normalización:** adaptadores Python para DENUE, ENOE y vacantes.
3. **Dominio:** cálculo de snapshot de mercado laboral.
4. **API:** FastAPI para health, datos territoriales, negocios y consultas futuras.
5. **Presentación:** dashboard HTML actual; evolución prevista a React/Vite.
6. **QA:** pytest, smoke test real opt-in, validación de esquema y generación determinista.

### Reglas de escalabilidad

- El dashboard consume un contrato, no columnas específicas de un CSV aislado.
- Las fuentes externas se encapsulan en adaptadores reemplazables.
- Cada registro conserva fuente, versión, periodo y estado de calidad.
- Las geometrías se referencian separadamente de los indicadores.
- La persistencia puede evolucionar de JSON/CSV a BigQuery GIS o PostGIS sin cambiar la semántica del indicador.

## 9. Criterios de aceptación

El MVP se considera funcional cuando:

- El dashboard se genera desde el repositorio con un comando documentado.
- Los filtros de país, ciudad, habilidad y métrica modifican la vista.
- La tabla muestra correctamente Estado–Ciudad y no usa HTML como base de datos.
- Saltillo, Monterrey y Guadalajara producen resultados reproducibles.
- El cálculo cumple `déficit = demanda - oferta` e `índice = demanda / oferta` cuando aplica.
- Un país sin datos se presenta como “sin datos”.
- JSON, CSV y GeoJSON son válidos y contienen metadatos mínimos.
- Las pruebas unitarias y de integración local pasan.
- La llamada real a DENUE se ejecuta solo con token configurado y falla de forma explícita si falta o es inválido.
- La interfaz identifica los valores sintéticos y no los presenta como estadística oficial.

## 10. Plan de construcción

### Fase 1 — Contrato y prototipo (actual)

- Mantener fixture de ciudades y habilidad AWS.
- Estabilizar esquema, generador, filtros, tabla y gráficos.
- Completar pruebas de cálculo y contrato.

### Fase 2 — Integración de fuentes

- Configurar token y cliente DENUE.
- Cargar extractos ENOE fechados y documentar variables elegidas.
- Incorporar vacantes autorizadas con fecha, ciudad y habilidad normalizada.
- Registrar provenance y estado de calidad por carga.

### Fase 3 — Persistencia y API de consulta

- Implementar almacenamiento seleccionado —BigQuery GIS o PostGIS—.
- Exponer endpoint de indicadores con filtros equivalentes al dashboard.
- Agregar paginación, caché controlado y observabilidad básica.

### Fase 4 — Validación piloto

- Validar Saltillo con revisión manual y fuentes oficiales.
- Comparar Monterrey y Guadalajara bajo la misma definición.
- Revisar sesgos, cobertura y estabilidad antes de publicar conclusiones.

## 11. Riesgos y controles

| Riesgo | Control del MVP |
|---|---|
| Confundir oferta ENOE con talento AWS | Etiquetar el dato como proxy y documentar la limitación. |
| Mezclar periodos | Exigir `period` y `source_version` en el contrato. |
| Comparar coberturas distintas | Mostrar fuente, fecha y estado por registro. |
| Token o API no disponible | Smoke test opt-in y modo fixture local. |
| HTML usado como persistencia | JSON/CSV versionados y esquema explícito. |
| Resultado visual sin evidencia | Tabla exportable y trazabilidad de cálculo. |

## 12. Próximo incremento recomendado

El siguiente incremento de construcción debe ser el **pipeline mínimo de datos reales para Saltillo**: una carga fechada de DENUE, un extracto ENOE documentado y una fuente de vacantes con habilidad normalizada. El resultado debe conservar el mismo contrato que el escenario sintético, ejecutar la misma batería QA y marcar cualquier dato no comparable antes de mostrarlo en el mapa.

