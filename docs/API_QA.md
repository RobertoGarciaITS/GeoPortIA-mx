# API QA y guía de configuración

## Objetivo

Esta guía deja la API lista para copiar, configurar y ejecutar. La suite actual valida el contrato HTTP local sin necesidad de una cuenta GCP.

## Pruebas incluidas

| Área | Cobertura |
|---|---|
| Disponibilidad | `/health` responde `200` y `status=ok` |
| Contrato OpenAPI | Las cinco rutas baseline están publicadas |
| Datos | Existen exactamente 10 negocios, con IDs únicos y coordenadas válidas |
| Municipio | `cvegeo=05030`, Saltillo y geometría GeoJSON tipo `Polygon` o `MultiPolygon` |
| Detalle | Un negocio válido responde y uno inexistente responde `404` |
| Validación | Coordenadas y radio fuera de rango responden `422` |
| Proximidad | El caso de 2 km devuelve 5 negocios y el punto exacto devuelve 1 |
| Cálculo local | Distancia Haversine cero y simétrica |
| Configuración cloud | Modo BigQuery exige proyecto y dataset explícitos |

## Ejecutar QA local

Desde la raíz:

```powershell
pytest -q
python -m compileall -q apps/api
git diff --check
```

Resultado esperado:

```text
15 passed
```

Para levantar la API:

```powershell
cd apps/api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="."
uvicorn app.main:app --reload --port 8000
```

Comprobaciones manuales:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/api/businesses
Invoke-RestMethod "http://localhost:8000/api/nearby?lat=25.438&lng=-100.973&radius_m=2000"
```

## Configuración local sin GCP

No definas `GEOOPPORTUNITY_USE_BIGQUERY`. La API leerá:

```text
data/sample/businesses_10.csv
data/sample/municipality_saltillo.geojson
```

Este modo sirve para desarrollo, pruebas y revisión del contrato.

## Configuración con BigQuery

Define todas las variables:

```powershell
$env:BIGQUERY_PROJECT="tu-proyecto-gcp"
$env:BIGQUERY_DATASET="geoopportunity"
$env:GEOOPPORTUNITY_USE_BIGQUERY="1"
```

Autentica la cuenta de desarrollo con Application Default Credentials o usa la identidad administrada de Cloud Run. Después:

```powershell
python scripts/ingest.py
uvicorn app.main:app --reload --port 8000
```

La tabla debe existir con el esquema de [sql/create_tables.sql](../sql/create_tables.sql). La consulta de proximidad está en [sql/nearby_businesses.sql](../sql/nearby_businesses.sql).

## QA de integración pendiente

Estas verificaciones requieren credenciales y servicios externos; no deben marcarse como aprobadas por tener pruebas unitarias verdes:

- Consulta real contra BigQuery.
- Consulta real contra la tabla de municipios en BigQuery.
- Carga de Google Maps JavaScript API.
- Respuesta WMS de INEGI en navegador.
- Build y ejecución Docker.
- Alcance público de Cloud Run.

## Criterio de aceptación

La API está lista para copiar y configurar cuando:

1. `pytest -q` pasa.
2. `/docs` y `/openapi.json` cargan.
3. `/api/businesses` devuelve 10 registros en modo fixture.
4. `/api/nearby` devuelve el resultado determinista esperado.
5. En modo BigQuery, faltantes de configuración producen un error explícito.
6. Las credenciales reales se inyectan por entorno y no se agregan al repositorio.

## Actualizar la geometría oficial

```powershell
python scripts/fetch_municipality.py
pytest -q
```

El script valida que INEGI devuelva exactamente el municipio `05030`, llamado Saltillo, con una geometría `Polygon` o `MultiPolygon`. Conserva la respuesta original y genera el archivo normalizado que consume la API.
