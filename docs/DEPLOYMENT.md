# Despliegue

1. Crear dataset BigQuery y reemplazar `${PROJECT_ID}`/`${DATASET}` en `sql/create_tables.sql`.
2. Cargar el fixture con `BIGQUERY_PROJECT=... python scripts/ingest.py`.
3. Construir y publicar `docker/Dockerfile` en Artifact Registry.
4. Ejecutar Cloud Run con `BIGQUERY_PROJECT`, `BIGQUERY_DATASET`, `GEOOPPORTUNITY_USE_BIGQUERY=1` y una identidad con permisos mínimos de consulta.
5. Configurar la clave restringida de Google Maps en el frontend según el proveedor de hosting.

No se incluyen secretos ni se ejecuta un despliegue automático sin credenciales explícitas.
