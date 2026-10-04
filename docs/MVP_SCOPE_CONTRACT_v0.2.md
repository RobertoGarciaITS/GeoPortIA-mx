# GeoPortIA Intelligence Map — contrato de alcance del MVP

**Contract ID:** `GEOOPPORTUNITY-INTELLIGENCE-MAP-MVP-001`  
**Versión:** `0.2`  
**Estado:** construcción y validación  
**Contrato relacionado:** `GEOOPPORTUNITY-BASELINE-001`

## 1. Definición del producto

GeoPortIA Intelligence Map es un sistema de inteligencia geoespacial y laboral que permite explorar la relación entre territorio, unidades económicas, talento disponible y demanda de habilidades.

El MVP no es todavía una plataforma nacional ni un sistema predictivo. Es un producto de validación que debe demostrar un flujo reproducible de datos, análisis y visualización para una ciudad de referencia.

## 2. Problema que intenta resolver

La información sobre empresas, geografía, población trabajadora, habilidades y vacantes suele estar separada en fuentes, formatos y niveles geográficos distintos. Esto dificulta responder de forma rápida y auditable:

> ¿En qué ciudad o territorio existe una posible brecha entre las capacidades disponibles y las habilidades que requieren las empresas?

## 3. Objetivo del MVP

Demostrar que un analista puede seleccionar una ciudad y una habilidad, revisar sus fuentes y periodo, observar oferta y demanda, calcular una señal de déficit y comparar el resultado con otras ciudades bajo la misma definición.

## 4. Caso de uso de referencia

```text
Habilidad: AWS
Ciudades: Saltillo, Monterrey y Guadalajara
Fuentes previstas: DENUE, ENOE y vacantes autorizadas
Salida: mapa, tabla, gráficos, JSON y CSV
```

Los valores actuales del ejemplo son sintéticos o controlados. No constituyen evidencia de una escasez real.

## 5. Alcance incluido

### Núcleo geoespacial

- Saltillo como municipio de referencia.
- Diez negocios controlados.
- Geometría oficial de INEGI.
- Consulta de proximidad por radio.
- API REST y frontend React/Vite.
- Fixtures locales y SQL preparado para BigQuery GIS.

### Extensión laboral

- Normalización de registros DENUE.
- Lectura de extractos ENOE agregados y no identificables.
- Lectura de vacantes con fecha, geografía y habilidad.
- Cálculo de oferta, demanda, déficit e índice de escasez.
- Comparación sintética entre ciudades.
- Dashboard demostrativo con filtros, tabla y gráficos.
- Exportación de contrato JSON y CSV.
- Pruebas unitarias y smoke tests opt-in.

### Entorno técnico

- Dev Container/Codespaces para desarrollo.
- GitHub Actions para pruebas.
- Dockerfile y Cloud Build preparados.
- Cloud Run como destino previsto, todavía no validado productivamente.

## 6. Alcance excluido

- Cobertura nacional operativa.
- Actualización automática de todas las fuentes.
- Endpoints laborales integrados en la API principal.
- Dashboard laboral integrado en el frontend React principal.
- Predicción de demanda o empleo.
- IA, machine learning o scoring propietario.
- Recomendación automatizada de inversión, contratación o candidatos.
- Autenticación, roles, pagos y multi-tenant.
- Google Places, Google Routes, PostGIS, Redis, GKE y streaming.
- Publicación productiva sin revisión de fuentes, metodología y seguridad.

## 7. Definición de indicadores

Para una geografía `g`, habilidad `s` y periodo `t`:

```text
oferta(g,s,t) = talento disponible observado o estimado bajo una definición documentada
demanda(g,s,t) = vacantes o puestos observados en una fuente autorizada
déficit(g,s,t) = demanda - oferta
índice(g,s,t) = demanda / oferta, cuando oferta > 0
```

El índice es una señal exploratoria. No es una probabilidad, pronóstico ni diagnóstico causal.

## 8. Estados de evidencia

| Estado | Significado |
|---|---|
| `synthetic` | Valor creado para probar flujo, interfaz o cálculo. |
| `controlled` | Fixture basado en una estructura de datos definida, sin afirmar medición oficial. |
| `official` | Dato obtenido de una fuente oficial con fecha y consulta documentadas. |
| `estimated` | Resultado derivado mediante una metodología explícita. |
| `stale` | Dato cuya fecha de actualización ya no cumple la política definida. |

La interfaz no debe presentar `synthetic` o `controlled` como resultado oficial.

## 9. Criterios de aceptación

El MVP integrado puede declararse validado cuando:

1. El baseline geoespacial conserva sus pruebas y resultados deterministas.
2. Los indicadores laborales cumplen el contrato JSON versionado.
3. El cálculo de déficit e índice coincide con pruebas unitarias.
4. Cada dato tiene fuente, periodo, versión y estado de evidencia.
5. La combinación ciudad–habilidad sin datos se muestra como “sin datos”, no como cero.
6. Saltillo, Monterrey y Guadalajara pueden compararse bajo la misma definición.
7. API, dashboard y exportaciones muestran los mismos valores.
8. Se valida al menos un conjunto real de DENUE y una fuente laboral autorizada.
9. Se documentan las limitaciones de ENOE y la cobertura de vacantes.
10. La imagen se construye y `/health` responde en un ambiente staging.

## 10. Gobernanza del cambio

Un cambio requiere nueva versión o change request si modifica:

- fuente o definición de indicadores;
- nivel geográfico;
- fórmula de oferta, demanda, déficit o índice;
- contrato JSON;
- endpoints públicos;
- modelo de persistencia;
- alcance de usuarios o decisiones soportadas;
- despliegue o controles de seguridad.

## 11. Evidencia actual y pendiente

### Existe

- 30 pruebas automatizadas pasando en el entorno local.
- Fixtures controlados de DENUE, ENOE, vacantes e indicadores.
- Cliente DENUE con manejo de token, error y límite.
- Scripts de dashboard y comparación de ciudades.
- Docker, Codespaces y Cloud Build configurados.

### Pendiente

- Token DENUE válido y ejecución real documentada.
- Consulta real de BigQuery GIS.
- API laboral integrada al backend.
- Frontend React conectado a indicadores laborales.
- Build Docker ejecutado con daemon o Cloud Build.
- Despliegue de staging en Cloud Run.
- Validación con usuarios objetivo.

