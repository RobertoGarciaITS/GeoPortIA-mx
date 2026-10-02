# Validación y evidencia

## Validación local

```bash
cd apps/api
pytest -q
```

El caso determinista usa `lat=25.438`, `lng=-100.973`, `radius_m=2000` y espera 5 negocios. El conteo se verifica de forma independiente mediante la fórmula Haversine en `app.services.data.distance_m`; en GCP, la consulta equivalente es `ST_DWITHIN` en `sql/nearby_businesses.sql`.

## Gate V0.1

- [x] Fixture reproducible de 10 negocios
- [x] Municipio y geometría de referencia
- [x] FastAPI `/health`, `/businesses`, detalle y `/nearby`
- [x] Frontend React/Vite con marcadores, radio y panel
- [x] SQL BigQuery GIS y script de ingestión
- [x] Dockerfile y Dev Container
- [ ] BigQuery ejecutado con credenciales del proyecto
- [ ] Google Maps JavaScript API configurada
- [ ] Imagen publicada en Artifact Registry / Cloud Run

Los tres últimos puntos requieren acceso GCP/Maps del propietario y no se declaran PASS sin evidencia externa.
