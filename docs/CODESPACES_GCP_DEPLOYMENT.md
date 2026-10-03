# Flujo Codespaces → GCP

Este documento define el camino operativo del MVP: desarrollar y probar en un Dev Container/Codespace, construir una imagen reproducible y desplegar la API en Cloud Run. La interfaz web puede permanecer como artefacto estático durante la fase de construcción; la API es el primer componente desplegable.

El Codespace se configura para el free tier: ejecuta edición, Python, Node, pruebas y generación de artefactos. No instala Docker-in-Docker; las imágenes se construyen remotamente con Cloud Build cuando se habilite el proyecto GCP.

## 1. Principio de operación

```text
Codespace / Dev Container
        ↓ pytest + build web
GitHub Actions
        ↓ imagen Docker
Artifact Registry
        ↓ Cloud Run
API GeoPortIA
```

El modo local usa fixtures versionados y no requiere credenciales GCP. La integración BigQuery, DENUE y Google Maps se habilita por variables de entorno y secretos del entorno; nunca se deben guardar tokens en Git.

## 2. Desarrollo en Codespaces

El archivo [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json) instala Python, Node y Google Cloud CLI. Esta configuración evita el daemon Docker local para reducir memoria y almacenamiento.

```bash
pip install -r apps/api/requirements.txt
export PYTHONPATH=apps/api
pytest -q apps/api/tests
python scripts/generate_city_labor_dashboard.py
cd apps/web && npm install && npm run build
```

Para ejecutar la API localmente:

```bash
export PYTHONPATH=apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El frontend usa `VITE_API_BASE_URL=http://localhost:8000`. En Codespaces se debe utilizar la URL reenviada del puerto 8000 cuando el frontend se ejecute desde otra URL.

## 3. Variables por entorno

### Local/Codespaces

```text
BIGQUERY_PROJECT=
BIGQUERY_DATASET=geoopportunity
GEOOPPORTUNITY_USE_BIGQUERY=0
INEGI_DENUE_TOKEN=
CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Cloud Run

```text
BIGQUERY_PROJECT=proyecto-gcp
BIGQUERY_DATASET=geoopportunity
GEOOPPORTUNITY_USE_BIGQUERY=1
INEGI_DENUE_TOKEN=<secret>
CORS_ALLOW_ORIGINS=https://dominio-del-frontend
```

`GOOGLE_MAPS_API_KEY` y `VITE_GOOGLE_MAPS_API_KEY` pertenecen al frontend. La clave del navegador debe tener restricciones por dominio y APIs mínimas; nunca debe usarse como secreto del backend.

## 4. Validación antes de desplegar

```bash
export PYTHONPATH=apps/api
pytest -q apps/api/tests
python scripts/generate_city_labor_dashboard.py
# La construcción Docker se valida en Cloud Build cuando GCP esté habilitado.
```

Comprobar `http://localhost:8000/health` y la documentación en `/docs`. El smoke test real de DENUE es opt-in y requiere token válido; el comportamiento por defecto sigue siendo local y reproducible.

## 5. Configuración GCP inicial

Crear o seleccionar un proyecto y habilitar Cloud Build, Artifact Registry, Cloud Run Admin y Secret Manager cuando se activen tokens.

Crear el repositorio Docker una sola vez:

```bash
gcloud artifacts repositories create geoportia \
  --repository-format=docker \
  --location=us-central1
```

El archivo [`cloudbuild.yaml`](../cloudbuild.yaml) construye, publica y despliega la API en Cloud Run:

```bash
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions=_REGION=us-central1,_SERVICE=geoportia-api,_CORS_ALLOW_ORIGINS=https://dominio-del-frontend
```

La imagen usa el SHA del commit (`$SHORT_SHA`) y el contenedor escucha en el puerto 8080. El despliegue público es apropiado solo para este MVP; antes de producción se deben agregar autenticación, límites de consumo, logging estructurado y políticas de acceso.

## 6. Gates de CI/CD

El workflow [`test.yml`](../.github/workflows/test.yml) debe ser el gate mínimo de cada pull request:

1. pruebas unitarias de API;
2. build del frontend;
3. generación reproducible de artefactos;
4. construcción remota de imagen Docker con Cloud Build;
5. despliegue únicamente desde la rama autorizada y con aprobación.

La primera etapa no despliega automáticamente a producción. Se recomienda separar `geoportia-api-staging` y `geoportia-api-prod` cuando se agregue CD.

## 7. Decisión de arquitectura para esta fase

- **Ahora:** fixture + FastAPI + Codespaces + Cloud Run opcional.
- **Siguiente:** BigQuery GIS como persistencia administrada y Secret Manager para DENUE.
- **Después:** frontend estático versionado con una URL configurada hacia la API de staging.

Esta separación permite probar el producto en Codespaces sin bloquearse por credenciales GCP y evita convertir el HTML generado en la base de datos del sistema.
