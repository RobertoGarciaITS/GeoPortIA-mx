# GeoOpportunity MX — Saltillo V0.1

Micro-MVP geoespacial: un municipio, diez negocios y una consulta real de proximidad. El proyecto sigue el contrato `GEOOPPORTUNITY-BASELINE-001`.

## Ejecutar localmente

```bash
cd apps/api
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda en `http://localhost:8000` y la documentación en `/docs`. Para el frontend:

```bash
cd apps/web
npm install
npm run dev
```

Sin credenciales GCP la API usa el fixture versionado de 10 registros. Con `BIGQUERY_PROJECT` y `BIGQUERY_DATASET` configurados, usa BigQuery para los negocios y conserva el mismo contrato REST.

## Endpoints

- `GET /health`
- `GET /api/municipality`
- `GET /api/businesses`
- `GET /api/businesses/{id}`
- `GET /api/nearby?lat=25.438&lng=-100.973&radius_m=2000`

## Alcance

Incluye Saltillo, una geometría municipal de referencia, fixture DENUE de 10 registros, FastAPI, React/Vite, consulta `ST_DWITHIN` en SQL, Docker y documentación. No incluye scoring, IA, autenticación, PostGIS, GKE ni expansión geográfica.

Consulta [docs/VALIDATION.md](docs/VALIDATION.md) para la evidencia y los pasos de validación con GCP.
