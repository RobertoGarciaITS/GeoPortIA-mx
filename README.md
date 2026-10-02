# GeoOpportunity MX — Saltillo V0.1

Micro-MVP geoespacial: un municipio, diez negocios y una consulta reproducible de proximidad. El proyecto sigue el contrato `GEOOPPORTUNITY-BASELINE-001` y separa tres responsabilidades:

```text
INEGI / DENUE → datos y cartografía oficial
BigQuery GIS  → GEOGRAPHY y análisis espacial
FastAPI       → contrato REST
React/Vite    → mapa, marcadores y resultados
```

## Estado del proyecto

Implementado y publicado en `main`:

- API FastAPI con health check, municipio, negocios, detalle y proximidad.
- Fixture controlado de exactamente 10 negocios.
- SQL BigQuery GIS con `ST_DWITHIN`.
- Frontend React + TypeScript + Vite.
- Integración preparada con Google Maps JavaScript API.
- Capa WMS municipal de INEGI: `Sitio_Inegi:Municipal`.
- Dockerfile, Dev Container, CI y documentación de validación.

Pendiente para declarar V0.1 validado: configurar credenciales GCP/Maps, cargar geometría oficial de INEGI, ejecutar BigQuery y publicar Cloud Run.

## Estructura

```text
apps/api/       FastAPI, modelos, servicios y pruebas
apps/web/       React/Vite y capa WMS de INEGI
data/sample/    fixture de 10 negocios y geometría local
sql/            DDL y consultas BigQuery GIS
scripts/        ingestión a BigQuery
docker/         imagen de ejecución
docs/           arquitectura, datos, despliegue y validación
```

## Ejecutar localmente

### API

```bash
cd apps/api
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
$env:PYTHONPATH="."
uvicorn app.main:app --reload --port 8000
```

La API queda en `http://localhost:8000`. Documentación automática:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI: `http://localhost:8000/openapi.json`

Sin configuración de BigQuery, la API usa el fixture versionado. Para usar BigQuery:

```text
BIGQUERY_PROJECT=tu-proyecto
BIGQUERY_DATASET=geoopportunity
GEOOPPORTUNITY_USE_BIGQUERY=1
```

### Frontend

```bash
cd apps/web
npm install
npm run dev
```

Variables frontend:

```text
VITE_API_BASE_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=tu-clave-restringida
```

La clave debe estar restringida por HTTP referrers y solo debe habilitar las APIs necesarias. No se debe guardar una clave real en Git.

## API REST

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/health` | Verificar disponibilidad |
| `GET` | `/api/municipality` | Obtener Saltillo y su geometría |
| `GET` | `/api/businesses` | Obtener los 10 negocios |
| `GET` | `/api/businesses/{id}` | Obtener un negocio |
| `GET` | `/api/nearby?lat=25.438&lng=-100.973&radius_m=2000` | Buscar negocios dentro de un radio en metros |

La consulta espacial oficial de producción está en [sql/nearby_businesses.sql](sql/nearby_businesses.sql):

```sql
WHERE ST_DWITHIN(
  geography,
  ST_GEOGPOINT(@lng, @lat),
  @radius_m
)
```

## INEGI + Google Maps

El frontend utiliza Google Maps JavaScript API como mapa interactivo y agrega la capa municipal oficial de INEGI mediante WMS:

```text
https://mapas.inegi.org.mx/geoserver/wms
LAYERS=Sitio_Inegi:Municipal
```

La capa WMS es cartográfica. Los negocios y el resultado de proximidad provienen de la API propia respaldada por BigQuery. No se debe confundir la capa visual de INEGI con la fuente analítica de negocios.

## Pruebas y validación

```bash
cd ../..
$env:PYTHONPATH="apps/api"
pytest -q apps/api/tests
```

El caso determinista usa `lat=25.438`, `lng=-100.973`, `radius_m=2000` y espera 5 negocios. Consulta [docs/VALIDATION.md](docs/VALIDATION.md) para el gate completo.

Para ejecutar la matriz QA, revisar [docs/API_QA.md](docs/API_QA.md).

## Documentación oficial de referencia

### Cartografía y APIs de INEGI

- [API de mapas de INEGI](https://www.inegi.org.mx/servicios/api_map.html): Google Maps, capas municipales/estatales, carga WMS y ejemplos.
- [MxSIG de INEGI](https://www.inegi.org.mx/servicios/mxsig.html): plataforma, WMS, WMTS, REST y componentes de publicación.
- [Repositorio oficial MxSIG](https://git.inegi.org.mx/mxsig/mxsig): código, configuración y operación de MxSIG.
- [API del DENUE](https://www.inegi.org.mx/servicios/api_denue.html): consulta de unidades económicas y documentación de acceso.
- [Catálogo Único de Claves Geoestadísticas](https://www.inegi.org.mx/servicios/catalogounico.html): claves `cvegeo` y referencias territoriales.
- [Servicio Web de Información Geográfica](https://www.inegi.org.mx/servicios/wsinfogeo/default.html): servicios del Mapa Digital de México.

### Google Maps JavaScript API

- [Descripción general](https://developers.google.com/maps/documentation/javascript/overview?hl=es-419): capacidades, capas y límites administrativos.
- [Agregar un mapa a una página web](https://developers.google.com/maps/documentation/javascript/add-google-map?hl=es): carga e inicialización recomendadas.
- [Configurar una clave de API](https://developers.google.com/maps/documentation/javascript/get-api-key?hl=es): proyecto, facturación, habilitación y restricciones.
- [Referencia de Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/reference?hl=es): clases, eventos, mapas, overlays y tipos.
- [Uso y facturación](https://developers.google.com/maps/documentation/javascript/usage-and-billing?hl=es-419): SKUs y costos de carga de mapas.

### Geoespacial y backend

- [Datos geoespaciales en BigQuery](https://cloud.google.com/bigquery/docs/geospatial-data): `GEOGRAPHY`, WKT, GeoJSON, carga, clustering y exportación.
- [Funciones geográficas de BigQuery](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions): `ST_GEOGPOINT`, `ST_WITHIN`, `ST_INTERSECTS`, `ST_DWITHIN` y `ST_ASGEOJSON`.
- [Primeros pasos con FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/): rutas, OpenAPI, Swagger UI y ReDoc.
- [Seguridad en FastAPI](https://fastapi.tiangolo.com/tutorial/security/first-steps/): referencia para futuras APIs protegidas; no activar autenticación en V0.1.

### Frontend

- [Aprender React](https://react.dev/learn): componentes, estado y efectos.
- [Instalación de React](https://react.dev/learn/installation): integración y alternativas actuales.
- [Guía de Vite](https://vite.dev/guide/): servidor de desarrollo, build y configuración.

## Reglas de alcance

V0.1 no incluye scoring, IA, autenticación, pagos, Google Places, Google Routes, PostGIS, Redis, GKE, streaming ni cobertura nacional. Cualquier expansión requiere un change request y una nueva versión del baseline.
