# Contrato de datos

`businesses_10.csv` contiene exactamente 10 registros controlados, con `business_id`, procedencia DENUE, nombre, SCIAN, actividad, rango de empleados, coordenadas, municipio y fuente. Las coordenadas generan `POINT(longitude latitude)` en BigQuery.

La geometría municipal está versionada en `data/sample/municipality_saltillo.geojson` y proviene del servicio oficial del Catálogo Único de Claves Geoestadísticas de INEGI para `cvegeo=05030`. La fuente cruda se conserva en `data/source/municipality_saltillo_inegi_2025.json` y puede regenerarse con `python scripts/fetch_municipality.py`.

Fuente oficial:

```text
https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/05030
```

El servicio reporta Marco Geoestadístico de diciembre de 2025. La geometría se normaliza como GeoJSON longitude/latitude sin el miembro `crs`, para su carga posterior a BigQuery `GEOGRAPHY`; la respuesta original conserva el metadato CRS entregado por INEGI.
