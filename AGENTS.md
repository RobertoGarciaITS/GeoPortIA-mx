# AGENTS.md

## Objetivo

GeoPortIA mantiene dos niveles de alcance:

- `GEOOPPORTUNITY-BASELINE-001`: vertical slice geoespacial de Saltillo, 10 negocios, una consulta de proximidad, API REST y mapa web.
- `GEOOPPORTUNITY-INTELLIGENCE-MAP-MVP-001`: extensión en construcción para relacionar territorio, empresas, talento, demanda y brechas laborales; su contrato está en `docs/MVP_SCOPE_CONTRACT_v0.2.md`.

El baseline geoespacial sigue siendo el núcleo técnico validable. La extensión laboral no debe declararse productiva hasta cumplir sus criterios de evidencia.

## Reglas de alcance

- Mantener el alcance del baseline: un municipio, diez negocios y una consulta espacial.
- Mantener la extensión laboral en modo fixture/controlado hasta validar fuentes reales, periodo, cobertura y metodología.
- No agregar scoring, IA, machine learning, autenticación, pagos, Google Places, Google Routes, PostGIS, Redis, GKE, streaming, app móvil o cobertura nacional sin change request.
- Si una mejora cambia fuentes, APIs, bases de datos, niveles geográficos o despliegue, documentar rationale, impacto y versión del baseline.
- No declarar BigQuery, Google Maps o Cloud Run como operativos sin evidencia ejecutada.

## Fuentes oficiales que deben preferirse

- Cartografía y capas: [INEGI API de mapas](https://www.inegi.org.mx/servicios/api_map.html) y [MxSIG](https://www.inegi.org.mx/servicios/mxsig.html).
- Negocios: [API DENUE](https://www.inegi.org.mx/servicios/api_denue.html).
- Claves territoriales: [Catálogo Único de Claves Geoestadísticas](https://www.inegi.org.mx/servicios/catalogounico.html).
- Mapa web: [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/overview?hl=es-419).
- Análisis: [BigQuery geoespacial](https://cloud.google.com/bigquery/docs/geospatial-data) y [funciones `GEOGRAPHY`](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions).

## Contratos técnicos

### Datos

- Usar `longitude`, `latitude` y `ST_GEOGPOINT(longitude, latitude)` para puntos.
- Guardar geometrías analíticas como BigQuery `GEOGRAPHY`.
- Usar `ST_ASGEOJSON` solo al preparar una respuesta para el frontend.
- Conservar `source`, `source_record_id`, fecha y claves territoriales.
- No reemplazar geometría oficial por polígonos dibujados a mano en datos productivos.

### Consultas espaciales

- La distancia de `ST_DWITHIN` está en metros.
- Para el caso baseline usar parámetros: `@lat`, `@lng`, `@radius_m`.
- Mantener la consulta parametrizada; nunca interpolar entrada del usuario en SQL.
- Preferir tablas persistidas con `GEOGRAPHY` y clustering geográfico cuando el volumen crezca.
- Validar al menos un resultado independientemente de la API.

### API FastAPI

- Definir rutas en `apps/api/app/main.py` o módulos de rutas coherentes.
- Usar modelos Pydantic para respuestas y parámetros.
- Mantener `/health` sin dependencia de BigQuery.
- Conservar `/docs`, `/redoc` y `/openapi.json` funcionando.
- Devolver `404` para negocios inexistentes y errores de validación HTTP estándar para coordenadas/radios inválidos.
- Consultar [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) antes de introducir patrones nuevos.

### Frontend y mapas

- Usar React + TypeScript + Vite; consultar [React Learn](https://react.dev/learn) y la [guía de Vite](https://vite.dev/guide/).
- Cargar Google Maps con una clave restringida y nunca incluir claves en código, commits o logs.
- Consumir WMS de INEGI como capa cartográfica; consumir la API propia para negocios y análisis.
- Mantener coordenadas en WGS84 para consultas y dejar la reproyección visual al mapa.
- Usar la documentación de [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/add-google-map?hl=es) y su [referencia](https://developers.google.com/maps/documentation/javascript/reference?hl=es).

## Configuración y secretos

- Copiar `.env.example` a `.env` solo localmente.
- Nunca cometer `.env`, credenciales JSON, tokens, API keys reales ni service accounts.
- Restringir `VITE_GOOGLE_MAPS_API_KEY` por referrer y APIs habilitadas.
- Usar IAM de mínimo privilegio para BigQuery.

## Validación obligatoria antes de entregar

```bash
$env:PYTHONPATH="apps/api"
pytest -q apps/api/tests
python -m compileall -q apps/api
cd apps/web
npm run build
```

Además:

- Revisar `git diff --check`.
- Verificar que `/health` responde.
- Verificar que `/api/businesses` devuelve exactamente 10 registros en V0.1.
- Verificar que `/api/nearby` coincide con la validación independiente.
- Si se modifican mapas, revisar visualmente la capa INEGI, marcadores, radio, leyenda y panel.
- Documentar cualquier prueba no ejecutada y la razón.

## Flujo de cambio

1. Leer el contrato y la documentación oficial relevante.
2. Inspeccionar el código y las pruebas existentes.
3. Implementar el cambio mínimo dentro del alcance.
4. Ejecutar pruebas y validaciones.
5. Actualizar documentación y `.env.example` si cambia la configuración.
6. Crear un commit descriptivo; hacer push solo cuando el usuario lo autorice.
