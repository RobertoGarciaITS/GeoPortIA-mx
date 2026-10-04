# Tesis e hipótesis de validación del MVP

**Producto:** GeoPortIA Intelligence Map  
**Contrato:** `GEOOPPORTUNITY-INTELLIGENCE-MAP-MVP-001`  
**Estado:** hipótesis por revisar

## 1. Tesis principal

> Si se integran cartografía oficial, unidades económicas y señales laborales en una vista geográfica auditable, entonces los equipos de desarrollo económico, capacitación y planeación podrán identificar y priorizar oportunidades regionales más rápido que usando consultas separadas, hojas de cálculo y reportes estáticos.

La tesis contiene tres supuestos que deben probarse por separado:

```text
Datos trazables
        +
Experiencia de exploración clara
        +
Indicadores útiles para una decisión
        ↓
Valor para el usuario
```

## 2. Hipótesis de problema

| ID | Hipótesis | Cómo revisarla | Evidencia mínima |
|---|---|---|---|
| P1 | Los usuarios necesitan cruzar empresas, territorio y talento para entender una oportunidad regional. | Entrevistas y observación de tareas actuales. | 3 de 5 usuarios describen el cruce como problema recurrente. |
| P2 | Los reportes actuales requieren integrar fuentes manualmente. | Revisar procesos, archivos y tiempos de análisis. | Evidencia de al menos 2 fuentes y un paso manual repetido. |
| P3 | Una vista por ciudad es más útil inicialmente que una cobertura nacional incompleta. | Prueba con usuarios de Saltillo/Coahuila. | Usuario puede formular una decisión concreta a escala ciudad. |

## 3. Hipótesis de valor

| ID | Hipótesis | Prueba | Métrica inicial |
|---|---|---|---|
| V1 | El mapa más tabla permite encontrar una señal relevante más rápido que un CSV aislado. | Comparar tarea con dashboard y con archivos. | Tiempo hasta primera conclusión y tasa de éxito. |
| V2 | La comparación de ciudades ayuda a priorizar dónde investigar. | Ejercicio Saltillo–Monterrey–Guadalajara. | 4 de 5 usuarios seleccionan una ciudad y explican por qué. |
| V3 | La trazabilidad aumenta la confianza en el indicador. | Mostrar fuente, periodo y estado sintético/oficial. | Usuario puede explicar el origen del dato sin asistencia. |
| V4 | Exportar JSON/CSV/QGIS extiende el valor a analistas técnicos. | Entregar exportación y observar reutilización. | Exportación consumida en al menos un flujo externo. |

## 4. Hipótesis de datos

| ID | Hipótesis | Riesgo |
|---|---|---|
| D1 | DENUE permite mapear suficientemente la concentración empresarial por actividad y territorio. | Cobertura, fecha y clasificación no representan demanda laboral directamente. |
| D2 | ENOE puede aportar contexto de población ocupada/disponible, pero no un inventario directo de talento AWS. | No sobreinterpretar la encuesta como oferta de una skill específica. |
| D3 | Las vacantes observadas son un proxy de demanda y deben conservar fecha y fuente. | Sesgo por plataforma, duplicados y cobertura desigual. |
| D4 | La definición de habilidad debe normalizarse antes de comparar ciudades. | AWS, cloud, DevOps y títulos relacionados no son automáticamente equivalentes. |

## 5. Hipótesis de producto

| ID | Hipótesis | Prueba técnica |
|---|---|---|
| T1 | El mismo contrato puede alimentar API, dashboard y exportaciones. | Contract test y comparación de snapshots. |
| T2 | El sistema puede cambiar fixtures por adaptadores oficiales sin reescribir la UI. | Ejecutar fuente fixture y fuente real detrás del mismo modelo. |
| T3 | Codespaces es suficiente para desarrollo y QA del MVP. | Crear entorno desde `.devcontainer` y repetir las pruebas. |
| T4 | Cloud Run es suficiente para el primer servicio API stateless. | Build, despliegue staging, health check y prueba de endpoint. |

## 6. Tesis de diferenciación

> En ciudades mexicanas, una herramienta abierta y trazable que conecte datos de INEGI con señales de talento y demanda puede ocupar un espacio entre los portales públicos descriptivos y las plataformas comerciales globales de workforce/location intelligence.

Esta tesis debe revisarse contra:

- DataMéxico.
- STPS y Observatorio Laboral.
- Lightcast.
- Chmura JobsEQ.
- ArcGIS Business Analyst.
- GURU y Vista Site Selection.

## 7. Plan de validación recomendado

### Fase A — Producto

- Probar el dashboard con cinco usuarios.
- Pedir una tarea concreta: “identificar dónde investigar una posible escasez de AWS”.
- Medir tiempo, errores, preguntas y confianza.

### Fase B — Datos

- Ejecutar DENUE con token válido para Saltillo.
- Documentar periodo y cobertura de ENOE.
- Integrar una fuente de vacantes autorizada.
- Comparar tres ciudades con la misma metodología.

### Fase C — Técnica

- Exponer indicadores mediante API.
- Conectar frontend React al contrato.
- Ejecutar build Docker en Cloud Build.
- Desplegar staging en Cloud Run.

### Fase D — Mercado

- Solicitar demos de competidores cercanos.
- Comparar el caso AWS en Saltillo.
- Entrevistar gobierno, educación y empresa.
- Revisar disposición de pago o intención de adopción.

## 8. Criterios para confirmar o rechazar la tesis

### Confirmación parcial

- Los usuarios completan la tarea.
- El mapa reduce tiempo de exploración.
- La fuente y el periodo son comprendidos.
- El resultado genera una siguiente acción verificable.

### Rechazo o ajuste

- Los usuarios solo necesitan una tabla, no un mapa.
- No existe una fuente de demanda suficientemente comparable.
- El indicador genera más confusión que utilidad.
- La definición de oferta por habilidad no puede defenderse.
- La decisión real ocurre a nivel de zona, industria o institución distinta a la ciudad.

## 9. Decisión que debe quedar al terminar la validación

El proyecto debe elegir una de estas rutas:

1. **Intelligence Map laboral:** priorizar brechas de habilidades y desarrollo económico.
2. **Location Intelligence empresarial:** priorizar empresas, territorios y selección de sitio.
3. **Data product/API:** priorizar contratos, fuentes y acceso programático.
4. **Herramienta de diagnóstico municipal:** priorizar reportes y decisiones de gobierno local.

No se recomienda ampliar funcionalidades hasta comprobar cuál de estas decisiones produce el mayor valor para usuarios reales.

