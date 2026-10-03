# GeoPortIA — QGIS Local Reference Baseline v0.1

**Contract ID:** `GEOPORTIA-QGIS-LOCAL-REFERENCE-BASELINE-001`  
**Status:** `DRAFT — NOT YET APPROVED`  
**Execution:** `GEO-QGIS-PREFLIGHT-001`

## Purpose

Establish a local, reproducible GIS reference implementation that can be compared with PyQGIS, BigQuery GIS, FastAPI and the GeoPortIA web map.

## Official source packages

National:

- `nal-QGis/QGis/MapaBaseMultiescala.gpkg`
- `nal-QGis/QGis/MapaBaseMultiescala.qgz`

Coahuila:

- `coah-QGis/Coahuila_de_Zaragoza/mapa_base.gpkg`
- `coah-QGis/Coahuila_de_Zaragoza/Coahuila_de_Zaragoza.qgz`

Hashes are recorded in `artifacts/qgis_preflight/file_inventory.csv` and `.json`.

## Evidence baseline

Both GeoPackages pass SQLite `PRAGMA integrity_check`, with 29 spatial layers in the national package and 8 in the Coahuila package. Both QGIS projects are version `3.40.9-Bratislava`, use `EPSG:6372`, reference their local GeoPackages, and have no detected broken datasource references or print layouts.

The detailed inventories are in [artifacts/qgis_preflight/preflight_summary.md](../artifacts/qgis_preflight/preflight_summary.md).

## Saltillo reference

The source identifies Saltillo using:

```text
cve_ent = 05
cve_mun = 030
nomgeo = Saltillo
cvegeo = 05030
```

The Coahuila package has a `municipios` layer with 39 `MULTIPOLYGON` features. The national package has `municipios_4m` and `municipios_6m`, each with 2,478 `MULTIPOLYGON` features. All are stored in EPSG:6372.

## Layer policy

- `REUSE`: Coahuila `municipios` for the local Saltillo reference.
- `ADAPT`: national municipal layers after filtering and CRS transformation.
- `REFERENCE`: state boundaries, labels, national framing and contextual layers.
- `NOT_REQUIRED`: bathymetry and nonessential contextual layers for V0.1.

## Read-only source policy

The original INEGI `.gpkg` and `.qgz` files are authoritative read-only source artifacts. They must not be modified, renamed, re-saved, migrated or used as a container for derived data. They must not be committed or uploaded automatically.

## Derived-data policy

Any filtered municipality, selected places, buffer, analysis table, map image or PDF must be written outside the source GeoPackages, under a separate working/output directory.

## Expected local validation workflow

```text
latitude, longitude, radius_m, limit
  → reference point
  → metric-safe buffer
  → spatial selection
  → distance calculation
  → sort by distance
  → select N places
  → map
  → table
  → print layout
  → PDF
```

Initial smoke test: Saltillo, 3 places, radius 2,000 meters. This workflow is designed but was not executed during the preflight.

## CRS and cloud equivalence

The local reference layers use EPSG:6372. The GeoPortIA API and BigQuery `GEOGRAPHY` use longitude/latitude WGS84 semantics, so the next derived workflow must explicitly transform or export the selected geometry rather than assuming the local projected coordinates are directly interchangeable.

- QGIS/PyQGIS: independent local reference result.
- BigQuery GIS: equivalent `ST_DWITHIN` and `ST_DISTANCE` result.
- FastAPI: serialized result and GeoJSON boundary.
- Frontend: visual confirmation with Google Maps and INEGI WMS.

## Automation recommendation

Use the minimum reproducible mechanism:

1. Start with a standalone PyQGIS or `qgis_process` smoke test once a QGIS executable is available.
2. Keep the input source packages read-only.
3. Write outputs outside the source directories.
4. Compare local selected IDs/distances with BigQuery and FastAPI.

Model Designer can be added later for visual teaching value, but it should not replace a scriptable reference test.

## Known limitations

- QGIS desktop/CLI was not discoverable on PATH; package inspection used read-only SQLite/ZIP/XML parsing.
- No QGIS render, buffer, selection, print layout or PDF was executed.
- The package project version is QGIS 3.40.9, while the expected workstation statement mentioned QGIS 4.2; compatibility must be confirmed before opening/saving in another version.
- The source CRS EPSG:6372 must be handled explicitly before feeding geometries to BigQuery `GEOGRAPHY`.

## Exit gate

This document remains `DRAFT — NOT YET APPROVED`. Approval requires the local 3-place smoke test, independent distance comparison, explicit CRS transformation evidence, and a documented output directory outside the source packages.
