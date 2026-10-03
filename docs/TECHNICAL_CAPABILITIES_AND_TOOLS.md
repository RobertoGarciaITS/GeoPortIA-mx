# GeoPortIA Intelligence Map
## Diseño técnico, capacidades y herramientas

**Estado:** fase de construcción  
**Versión:** MVP-0.1  
**Entorno objetivo:** GitHub Codespaces → GitHub Actions → GCP

## 1. Propósito

Este documento define las capacidades técnicas y herramientas necesarias para construir, probar y desplegar GeoPortIA Intelligence Map. El diseño está orientado a mantener un mismo contrato entre datos, API, frontend y nube, comenzando con fixtures reproducibles y evolucionando hacia datos oficiales de INEGI, DENUE, ENOE y fuentes de vacantes.

## 2. Arquitectura de referencia

```text
┌──────────────────────────────────────────────────────────────┐
│ GitHub Codespace / Dev Container                            │
│ Python · Node · pytest · Vite · gcloud CLI                  │
└───────────────────────┬──────────────────────────────────────┘
                        │ commit / pull request
                        ▼
┌──────────────────────────────────────────────────────────────┐
│ GitHub Actions                                               │
│ tests API · build frontend · validación de contrato          │
└───────────────────────┬──────────────────────────────────────┘
                        │ build autorizado
                        ▼
┌──────────────────────────────────────────────────────────────┐
│ GCP                                                           │
│ Cloud Build → Artifact Registry → Cloud Run                   │
│ Secret Manager · BigQuery GIS · Cloud Logging                 │
└───────────────────────┬──────────────────────────────────────┘
                        ▼
                 Intelligence Map API
```

## 3. Principios técnicos

1. **Contrato antes que interfaz:** el frontend consume datos normalizados, no archivos ad hoc.
2. **Local primero:** el sistema debe funcionar sin credenciales usando fixtures versionados.
3. **Fuentes reemplazables:** DENUE, ENOE y vacantes se conectan mediante adaptadores separados.
4. **Trazabilidad:** cada indicador conserva fuente, periodo, versión y estado de calidad.
5. **Seguridad por entorno:** ningún token o clave privada se almacena en el repositorio.
6. **Escalamiento gradual:** Codespaces para construcción, Cloud Build para imágenes y Cloud Run para API.
7. **No confundir demostración con estadística oficial:** los datos sintéticos deben identificarse en API y UI.

## 4. Capacidades por componente

| Componente | Capacidades MVP | Evolución prevista |
|---|---|---|
| Backend | Health check, municipio, negocios, proximidad, indicadores laborales y OpenAPI | Consultas geográficas paginadas, autenticación, caché y observabilidad avanzada |
| Frontend | Mapa, filtros, tabla, tarjetas, gráficos y exportación | React modular, capas dinámicas, selección espacial y sesiones de análisis |
| Datos | JSON/CSV/GeoJSON, fixtures y contratos versionados | BigQuery GIS/PostGIS, cargas incrementales y catálogo de datos |
| Codespaces | Desarrollo, pruebas, scripts y vista local | Prebuilds y tareas automatizadas de desarrollo |
| CI | Pytest y build web | Contract tests, análisis estático, imagen y gates por ambiente |
| Cloud | Cloud Run, Artifact Registry y Cloud Build | Secret Manager, BigQuery, logging, alertas y ambientes staging/prod |

## 5. Backend

### 5.1 Tecnología

- Python 3.12.
- FastAPI para API REST y OpenAPI.
- Uvicorn como servidor ASGI.
- Pydantic para modelos y validación.
- Pytest para pruebas unitarias e integración local.
- `httpx` para clientes HTTP de fuentes externas.
- BigQuery GIS como persistencia administrada prevista.

Archivos principales:

- [apps/api/app/main.py](../apps/api/app/main.py)
- [apps/api/app/models/schemas.py](../apps/api/app/models/schemas.py)
- [apps/api/app/services/data.py](../apps/api/app/services/data.py)
- [apps/api/app/inegi/denue.py](../apps/api/app/inegi/denue.py)
- [apps/api/app/inegi/enoe.py](../apps/api/app/inegi/enoe.py)
- [apps/api/app/inegi/labor.py](../apps/api/app/inegi/labor.py)

### 5.2 Capacidades requeridas

- `GET /health` para disponibilidad.
- Endpoints de municipio y unidades económicas.
- Consulta de proximidad con latitud, longitud y radio.
- Cliente DENUE con token configurado por entorno.
- Lectura y validación de extractos ENOE.
- Cálculo reproducible de oferta, demanda, déficit e índice de escasez.
- Respuestas tipadas y documentación automática en `/docs` y `/openapi.json`.
- Modo fixture cuando BigQuery o tokens no están disponibles.
- CORS explícito mediante `CORS_ALLOW_ORIGINS`.

### 5.3 Reglas de backend

- No leer secretos desde código fuente.
- Validar rangos geográficos y límites de radio.
- No convertir errores de fuente en valores cero.
- Diferenciar “sin datos” de cero observado.
- Registrar `source`, `period`, `source_version` y `data_status`.
- Mantener adaptadores externos independientes del dominio laboral.

### 5.4 Contrato de indicador

```text
country_code, state_code, state_name, city_code, city_name,
skill_code, skill_name, period, supply, demand, deficit,
scarcity_index, geometry_ref, source, source_version, data_status
```

Estados mínimos: `synthetic`, `official`, `estimated`, `stale`.

## 6. Frontend y visualización

### 6.1 Tecnología

- React y TypeScript para la aplicación web evolucionada.
- Vite para desarrollo y build.
- D3.js para gráficos y geometrías del prototipo actual.
- Google Maps JavaScript API como integración cartográfica prevista.
- Capas WMS/MxSIG de INEGI para cartografía oficial cuando aplique.

Archivos y artefactos actuales:

- [apps/web/src/main.tsx](../apps/web/src/main.tsx)
- [apps/web/src/styles.css](../apps/web/src/styles.css)
- [artifacts/labor_comparison/city_labor_dashboard.html](../artifacts/labor_comparison/city_labor_dashboard.html)
- [scripts/generate_city_labor_dashboard.py](../scripts/generate_city_labor_dashboard.py)

### 6.2 Capacidades requeridas

- Selector de país, estado, ciudad, habilidad y métrica.
- Mapa con límites y clasificación por índice.
- Tabla Estado–Ciudad.
- Gráfico oferta frente a demanda.
- Gráfico de déficit o métrica elegida.
- Estado de carga, error y “sin datos”.
- Etiqueta visible para valores sintéticos.
- Diseño responsive y tabla accesible con teclado.
- URL de API configurable con `VITE_API_BASE_URL`.
- API key de Google Maps únicamente en el cliente y restringida por dominio.

### 6.3 Regla de separación

El HTML generado sirve como prototipo portable. En la siguiente etapa, el frontend debe obtener indicadores y GeoJSON desde la API o archivos versionados; no debe utilizar el HTML como base de datos.

## 7. Datos y geoespacial

### Fuentes

- INEGI Marco Geoestadístico: límites, localidades, áreas urbanas, manzanas y vialidades.
- DENUE: unidades económicas y ubicación.
- ENOE: contexto de población y empleo; requiere interpretación estadística.
- SNE u otra fuente autorizada: vacantes y demanda observable.

### Herramientas

- QGIS para inspección y validación visual.
- GeoJSON para intercambio web.
- CSV para interoperabilidad y auditoría.
- BigQuery `GEOGRAPHY` para consultas espaciales administradas.
- SQL versionado en [sql/](../sql/).

### Calidad mínima

- CRS documentado y conversión web a WGS84 cuando corresponda.
- Claves geográficas normalizadas.
- Periodo y fecha de carga obligatorios.
- Validación de geometrías antes de publicar.
- Conteos y muestras verificables.

## 8. GitHub Codespaces

### Propósito

Codespaces es el entorno de construcción y QA del MVP. Debe permitir trabajar sin una instalación local compleja y sin depender de credenciales GCP.

### Herramientas instaladas

- Python 3.12.
- Node.js 22 y npm.
- Google Cloud CLI.
- Extensiones Python, Pylance y ESLint.
- Git y Dev Container.

La configuración se encuentra en [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json).

### Operaciones permitidas

```bash
export PYTHONPATH=apps/api
pytest -q apps/api/tests
python scripts/generate_city_labor_dashboard.py
cd apps/web && npm run build
```

### Uso responsable del free tier

- No instalar Docker-in-Docker.
- No guardar datasets grandes dentro del Codespace.
- No dejar servidores ejecutándose cuando no se usan.
- Usar fixtures pequeños para pruebas.
- Ejecutar builds Docker en Cloud Build.
- Mantener artefactos grandes fuera del flujo diario de desarrollo.

## 9. Cloud GCP

### Servicios

| Servicio | Uso |
|---|---|
| Cloud Build | Construir y publicar imágenes desde el repositorio |
| Artifact Registry | Almacenar imágenes Docker versionadas |
| Cloud Run | Ejecutar la API HTTP sin administrar servidores |
| Secret Manager | Guardar tokens DENUE y credenciales sensibles |
| BigQuery GIS | Persistencia y consultas geoespaciales futuras |
| Cloud Logging | Logs de aplicación y despliegue |
| IAM | Separar permisos de desarrollo, build y ejecución |

### Requisitos de la imagen

- Escuchar en `0.0.0.0:8080`.
- Ser stateless.
- No escribir datos permanentes en el contenedor.
- Ejecutar como usuario no root.
- Usar variables de entorno para configuración.
- Tener `/health` como comprobación básica.

Archivos:

- [docker/Dockerfile](../docker/Dockerfile)
- [cloudbuild.yaml](../cloudbuild.yaml)
- [.dockerignore](../.dockerignore)

### Ambientes

| Ambiente | Fuente | Uso |
|---|---|---|
| Local/Codespace | Fixtures | Desarrollo y pruebas |
| Staging | Datos controlados/oficiales | Validación de integración |
| Producción | Datos oficiales aprobados | Servicio público o interno |

No se debe conectar el Codespace directamente a producción para pruebas normales.

## 10. Seguridad y configuración

Variables locales de referencia en `.env.example`:

```text
BIGQUERY_PROJECT=
BIGQUERY_DATASET=geoopportunity
GEOOPPORTUNITY_USE_BIGQUERY=0
INEGI_DENUE_TOKEN=
CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
VITE_API_BASE_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=
```

Reglas:

- `.env` no se versiona.
- Tokens de GCP y DENUE van en Secret Manager.
- Las claves de Google Maps tienen restricciones de referrer y APIs.
- Cloud Run usa una cuenta de servicio con mínimo privilegio.
- CORS de producción debe listar dominios conocidos, no `*`.
- Los datos personales no forman parte del MVP.

## 11. QA y observabilidad

### Gates mínimos

1. Validación JSON del Dev Container.
2. Unit tests de dominio y adaptadores.
3. Pruebas de API FastAPI.
4. Validación de contrato de indicadores.
5. Build del frontend.
6. Generación reproducible de dashboard y exportaciones.
7. Build de imagen en Cloud Build.
8. Smoke test de `/health` en staging.

### Métricas futuras

- Latencia p50/p95 por endpoint.
- Tasa de errores HTTP.
- Fecha de última carga por fuente.
- Porcentaje de registros sin geometría.
- Cobertura por ciudad y periodo.
- Estado de actualización de DENUE/ENOE/vacantes.

## 12. Criterios para avanzar a staging

El MVP puede pasar a staging cuando:

- Todas las pruebas locales pasan.
- La imagen se construye en Cloud Build.
- Cloud Run responde `/health`.
- CORS acepta únicamente el frontend autorizado.
- Los secretos no aparecen en logs ni repositorio.
- Los datos incluyen fuente, periodo y estado.
- El dashboard distingue sintético de oficial.
- Saltillo tiene un primer conjunto de datos reales documentado.

## 13. Fuera de alcance actual

- Kubernetes/GKE.
- Microservicios independientes.
- Streaming y tiempo real.
- IA predictiva.
- Autenticación completa y multi-tenant.
- Cobertura nacional automatizada.
- Garantías estadísticas derivadas únicamente del prototipo visual.

