# Comparación de escenarios laborales por ciudad

Ejecutar:

```powershell
python scripts/compare_city_labor_examples.py
python scripts/generate_city_labor_dashboard.py
```

El tablero incluye el selector de país `México`, `Canadá` y `Estados Unidos`. Actualmente solo México tiene datos de prueba; los otros países muestran “sin datos” hasta incorporar sus fuentes. La tabla incluye Estado, Ciudad, oferta, demanda, déficit e índice.

El diseño escalable usa `data/sample/labor_indicators_v1.json` como contrato de datos y genera HTML, CSV y GeoJSON como salidas. El HTML no es la fuente de verdad. El esquema futuro de persistencia está en `sql/labor_indicators_schema.sql`.

Salidas generadas:

- `artifacts/labor_comparison/city_labor_dashboard.html`: mapa, tabla, gráficos y selectores de ciudad, habilidad y métrica.
- `artifacts/labor_comparison/city_boundaries.geojson`: límites municipales oficiales transformados a WGS84.
- `artifacts/labor_comparison/city_labor_indicators.csv`: tabla para QGIS, Excel o Power BI.
- `artifacts/labor_comparison/city_labor_indicators.json`: datos normalizados para aplicaciones.
- `artifacts/labor_comparison/state_city_labor_indicators.json`: tabla jerárquica Estado–Ciudad en JSON.
- `artifacts/labor_comparison/state_city_labor_indicators.csv`: tabla jerárquica Estado–Ciudad en CSV.

## Resultado esperado del escenario AWS

| Ciudad | Oferta disponible | Demanda | Déficit | Índice de escasez | Interpretación |
|---|---:|---:|---:|---:|---|
| Saltillo | 3 | 8 | 5 | 2.67 | Escasez alta |
| Monterrey | 10 | 18 | 8 | 1.80 | Escasez moderada |
| Guadalajara | 15 | 12 | -3 | 0.80 | Equilibrio o superávit |

Este resultado únicamente prueba el comportamiento del modelo con escenarios controlados. No significa que esas ciudades tengan actualmente esos valores de AWS.

## Cómo interpretar el escenario

- Saltillo muestra el índice más alto porque la oferta disponible es pequeña frente a la demanda.
- Monterrey tiene más talento absoluto, pero también una demanda mayor.
- Guadalajara presenta más oferta disponible que demanda en este escenario.

El déficit absoluto no debe confundirse con el índice: Monterrey tiene un déficit mayor en número de puestos, mientras que Saltillo tiene una presión relativa mayor sobre su oferta disponible.

Para convertirlo en medición real hay que reemplazar los escenarios por DENUE, ENOE y vacantes fechadas de una fuente autorizada; mantener la misma definición de habilidad, periodo y geografía; y reportar precisión estadística y cobertura.
