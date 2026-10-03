"""QGIS step 04: locate Saltillo with an exact attribute query."""

from __future__ import annotations

from pathlib import Path


def _json_value(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def run(gpkg_path: str, layer_name: str = "municipios") -> dict:
    """Find the single Saltillo municipality using stable catalog keys."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsFeatureRequest, QgsVectorLayer
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")

    path = Path(gpkg_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {path}")

    uri = f"{path.as_posix()}|layername={layer_name}"
    layer = QgsVectorLayer(uri, f"step04_{layer_name}", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"La capa no pudo abrirse: {uri}")

    expression = '"cve_ent" = \'05\' AND "cve_mun" = \'030\' AND "nomgeo" = \'Saltillo\''
    request = QgsFeatureRequest().setFilterExpression(expression)
    matches = []
    field_names = [field.name() for field in layer.fields()]
    for feature in layer.getFeatures(request):
        matches.append(
            {
                "id": int(feature.id()),
                "attributes": {
                    name: _json_value(feature[name]) for name in field_names
                },
                "geometry_type": feature.geometry().type().name,
                "has_geometry": not feature.geometry().isEmpty(),
            }
        )

    if len(matches) != 1:
        raise RuntimeError(f"Se esperaba exactamente un Saltillo; se encontraron {len(matches)}.")

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "provider": layer.providerType(),
        "layer_name": layer_name,
        "path": str(path),
        "query": expression,
        "matched_count": len(matches),
        "match": matches[0],
        "visual_selection_changed": False,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\\archivo.gpkg').")
