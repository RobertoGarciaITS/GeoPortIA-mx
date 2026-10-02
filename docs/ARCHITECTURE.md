# Arquitectura V0.1

INEGI/DENUE → fixture normalizado → BigQuery `GEOGRAPHY` → FastAPI → React/TypeScript → mapa web. El modo local lee el fixture para permitir validación sin credenciales; producción activa el adaptador BigQuery con `GEOOPPORTUNITY_USE_BIGQUERY=1`.

El despliegue previsto es una imagen Docker en Cloud Run. GKE, Kubernetes, microservicios y servicios persistentes no forman parte de V0.1.
