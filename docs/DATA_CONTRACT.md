# Contrato de datos

`businesses_10.csv` contiene exactamente 10 registros controlados, con `business_id`, procedencia DENUE, nombre, SCIAN, actividad, rango de empleados, coordenadas, municipio y fuente. Las coordenadas generan `POINT(longitude latitude)` en BigQuery.

La geometría municipal está versionada en `data/sample/municipality_saltillo.geojson` como fixture de referencia derivado de INEGI. Antes de un despliegue productivo debe sustituirse por el archivo oficial descargado y conservarse su URL/fecha/hash.
