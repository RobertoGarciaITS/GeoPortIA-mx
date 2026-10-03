# Inventario y política de versionado del repositorio

**Estado:** diagnóstico inicial  
**Fecha:** 2026-10-03  
**Rama revisada:** `research/qgis-local-reference-preflight-001`

## Resultado ejecutivo

El repositorio contiene código funcional, documentación, fixtures pequeños, datos geoespaciales locales y fuentes externas de gran tamaño. El principal riesgo era subir accidentalmente la carpeta `794551163061_s/`, con aproximadamente 17.6 GB.

No se eliminaron ni movieron archivos. Se actualizó `.gitignore` para evitar que los datasets locales, MxSIG, carpetas QGIS y artefactos generados entren por accidente en futuros commits.

## Clasificación observada

| Grupo | Rutas | Tamaño observado | Política |
|---|---|---:|---|
| Código backend | `apps/api/app/`, `apps/api/tests/` | pequeño | Versionar |
| Código frontend | `apps/web/` | pequeño | Versionar |
| Scripts | `scripts/` | pequeño | Versionar |
| SQL y contratos | `sql/`, `data/contracts/` | pequeño | Versionar |
| Fixtures | `data/sample/` | pequeño | Versionar si no contienen datos sensibles |
| Documentación | `docs/`, `README.md`, `AGENTS.md` | pequeño | Versionar |
| Configuración | `.devcontainer/`, Docker, CI, `.env.example` | pequeño | Versionar |
| Datos masivos | `794551163061_s/` | ~17.6 GB | Ignorar; usar almacenamiento externo/manifiesto |
| Fuente externa MxSIG | `MxSIG/` | ~130 MB | Ignorar; documentar versión y origen |
| Datos QGIS locales | `coah-QGis/`, `nal-QGis/` | ~17 MB y ~0.4 MB | Ignorar por defecto; publicar solo muestras o resultados seleccionados |
| Artefactos | `artifacts/` | ~6 MB | Ignorar; regenerar con scripts |

## Archivos que sí deben formar parte del producto

```text
apps/api/
apps/web/
scripts/
sql/
data/contracts/
data/sample/                 # solo fixtures controlados
docs/
.devcontainer/
.github/
docker/
cloudbuild.yaml
README.md
AGENTS.md
.env.example
.env.inegi.example           # solo plantilla sin secretos
```

## Archivos que no deben subirse

```text
794551163061_s/
MxSIG/
coah-QGis/
nal-QGis/
artifacts/
.env
*.key
*.pem
credentials*.json
service-account*.json
```

## Regla para QGIS y MxSIG

El repositorio debe contener scripts, inventarios, metadatos y muestras mínimas. Las fuentes completas de cartografía se mantienen fuera de Git y se referencian mediante:

- nombre de fuente;
- versión o fecha;
- URL o ubicación de descarga;
- CRS;
- entidad y municipio;
- checksum cuando sea posible;
- procedimiento de regeneración.

## Regla para artifacts

Los archivos HTML, PDF, PNG, GeoJSON y CSV generados por scripts no son la fuente de verdad. Se regeneran mediante comandos documentados, por ejemplo:

```powershell
python scripts/generate_city_labor_dashboard.py
python scripts/qgis_export_saltillo_map.py
```

Si un resultado debe publicarse como evidencia, debe copiarse de forma explícita a un release, pull request o almacenamiento de artefactos, no entrar automáticamente con `git add .`.

## Flujo seguro antes de un commit

```powershell
git status --short
git diff --stat
git add <archivos-específicos>
git diff --cached --stat
git diff --cached --name-only
git commit -m "mensaje acotado"
```

No utilizar `git add .` mientras existan datos locales no clasificados.

## Próximo bloque autorizado para commit

El siguiente commit técnico puede incluir, previa validación:

- cliente y módulos INEGI;
- pruebas unitarias;
- contratos y fixtures pequeños;
- scripts reproducibles;
- documentación de integración laboral;
- configuración Codespaces/GCP.

Los datos geoespaciales masivos y artefactos generados deben permanecer fuera del commit.

