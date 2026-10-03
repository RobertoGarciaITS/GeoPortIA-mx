# Pruebas QGIS paso a paso

La automatización se ejecutará en pasos pequeños. Cada paso debe pasar antes de iniciar el siguiente.

## Paso 01 — conexión, apertura y liberación

Objetivo: verificar únicamente que PyQGIS y el proveedor OGR pueden abrir la capa `municipios` del GeoPackage de Coahuila en modo lectura.

Archivo:

```text
scripts/qgis_step_01_open_close.py
```

Fuente:

```text
coah-QGis/Coahuila_de_Zaragoza/mapa_base.gpkg
```

### Ejecución desde QGIS

1. Abre QGIS.
2. Abre `Plugins → Python Console`.
3. Ejecuta:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_01_open_close.py', encoding='utf-8').read(), globals())
```

4. Ejecuta la prueba:

```python
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg')
```

Resultado esperado:

```python
{
    'status': 'PASS',
    'provider': 'ogr',
    'layer_name': 'municipios',
    'opened': True,
    'read_features': False,
    'modified_source': False,
    'released': True
}
```

### Ejecución automatizada verificada

La prueba también fue ejecutada con QGIS 4.2.3 mediante:

```powershell
$q='C:\Program Files\QGIS 4.2.3'
$script='C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_01_open_close.py'
$gpkg='C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg'
$code="import os; os.add_dll_directory(r'$q\apps\Qt6\bin'); os.add_dll_directory(r'$q\apps\qgis\bin'); from qgis.core import QgsApplication; app=QgsApplication([],False); app.initQgis(); ns={}; exec(open(r'$script',encoding='utf-8').read(),ns); print(ns['run'](r'$gpkg')); app.exitQgis()"
& "$q\bin\python-qgis.bat" -c $code
```

Resultado observado el 2026-10-02: `PASS`. El detalle reproducible está en
`artifacts/qgis_preflight/step_01_result.json`.

### Qué valida

- La consola Python de QGIS tiene PyQGIS.
- QGIS tiene disponible el proveedor OGR.
- El archivo existe y es `.gpkg`.
- La capa `municipios` puede abrirse.
- La fuente no se modifica.
- La referencia de la capa se libera correctamente.

### Qué todavía no hace

- No lee entidades.
- No inspecciona atributos.
- No selecciona Saltillo.
- No crea capas temporales.
- No calcula buffers.
- No exporta archivos.
- No modifica el `.gpkg` ni el `.qgz`.

## Secuencia posterior

Solo después de que Paso 01 devuelva `PASS`:

1. Paso 02 — leer metadatos de la capa.
2. Paso 03 — leer campos y una muestra limitada.
3. Paso 04 — localizar `cve_ent=05`, `cve_mun=030`, `nomgeo=Saltillo`.
4. Paso 05 — crear el punto de referencia.
5. Paso 06 — seleccionar negocios dentro del radio.
6. Paso 07 — calcular distancias y ordenar.
7. Paso 08 — exportar resultados fuera del GeoPackage.

No se debe saltar directamente al análisis espacial.

## Paso 02 — lectura de metadatos

Archivo:

```text
scripts/qgis_step_02_layer_metadata.py
```

Ejecutar después de cargar el script del Paso 01:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_02_layer_metadata.py', encoding='utf-8').read(), globals())
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg')
```

El paso consulta solo metadatos: geometría, CRS, campos y extensión. No itera entidades, no selecciona registros y no escribe en el GeoPackage.

## Paso 03 — lectura de muestra limitada

Archivo:

```text
scripts/qgis_step_03_sample_features.py
```

Ejecutar después del Paso 02:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_03_sample_features.py', encoding='utf-8').read(), globals())
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg', limit=5)
```

La prueba lee como máximo cinco entidades, sus identificadores y atributos. No crea una selección en el lienzo ni modifica la fuente.

## Paso 04 — localizar Saltillo

Archivo:

```text
scripts/qgis_step_04_find_saltillo.py
```

Consulta exacta:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_04_find_saltillo.py', encoding='utf-8').read(), globals())
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg')
```

La consulta debe devolver exactamente un registro con `cve_ent=05`, `cve_mun=030` y `nomgeo='Saltillo'`. No cambia la selección visual de QGIS.

## Paso 05 — crear punto de referencia

Archivo:

```text
scripts/qgis_step_05_reference_point.py
```

Ejecución:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_05_reference_point.py', encoding='utf-8').read(), globals())
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg')
```

El punto se calcula con `pointOnSurface`, se valida que esté dentro de Saltillo y permanece únicamente en memoria.

## Paso 06 — consulta espacial por radio

Archivo:

```text
scripts/qgis_step_06_spatial_radius_query.py
```

Prueba inicial sobre la capa municipal, con radio de 10 km:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_06_spatial_radius_query.py', encoding='utf-8').read(), globals())
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg', target_layer_name='municipios', radius_m=10000)
```

Esta etapa devuelve IDs cercanos sin cambiar la selección visual del proyecto. Cuando exista la capa de negocios, se reutiliza pasando su nombre como `target_layer_name`.

## Paso 07 — calcular y ordenar distancias

Archivo:

```text
scripts/qgis_step_07_distance_order.py
```

Ejecución:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_07_distance_order.py', encoding='utf-8').read(), globals())
run(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg', target_layer_name='municipios', radius_m=10000)
```

La distancia se expresa en las unidades del CRS proyectado `EPSG:6372` y los resultados se ordenan ascendentemente.

## Paso 08 — exportar resultados fuera del GeoPackage

Archivo:

```text
scripts/qgis_step_08_export_results.py
```

Ejecución:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_step_08_export_results.py', encoding='utf-8').read(), globals())
run(
    r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg',
    r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\artifacts\qgis_preflight\step_08_results.csv',
    target_layer_name='municipios',
    radius_m=10000,
)
```

La salida es CSV UTF-8 con BOM. El script impide sobrescribir el GeoPackage.

## Exportación visual — mapa de Saltillo

Archivo:

```text
scripts/qgis_export_saltillo_map.py
```

Exportación automatizada a PNG:

```python
exec(open(r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\scripts\qgis_export_saltillo_map.py', encoding='utf-8').read(), globals())
run(
    r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\coah-QGis\Coahuila_de_Zaragoza\mapa_base.gpkg',
    r'C:\Users\Rober\projects\GeoPortIA\GeoPortIA-mx\artifacts\qgis_preflight\saltillo_map.png',
)
```

El resultado es una imagen independiente del GeoPackage, centrada en Saltillo.

## Exportación visual — PDF sin relleno

Archivo:

```text
scripts/qgis_export_saltillo_outline_pdf.py
```

El script genera una página A4 horizontal con fondo blanco, relleno transparente y solo el contorno negro de Saltillo.
