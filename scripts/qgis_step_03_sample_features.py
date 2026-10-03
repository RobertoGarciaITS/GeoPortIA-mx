"""QGIS step 03: read a bounded sample of vector features.

The test is read-only and deliberately limits the iterator. It does not
select features, start an edit session, export data, or write to the source.
"""

from __future__ import annotations

from pathlib import Path


def _json_value(value):
    """Convert common QGIS/Python attribute values to JSON-safe values."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def run(gpkg_path: str, layer_name: str = "municipios", limit: int = 5) -> dict:
    """Read at most ``limit`` features from a GeoPackage layer."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsFeatureRequest, QgsVectorLayer
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        raise ValueError("limit debe ser un entero entre 1 y 100")

    path = Path(gpkg_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {path}")
    if path.suffix.lower() != ".gpkg":
        raise ValueError(f"El archivo no tiene extensión .gpkg: {path}")

    uri = f"{path.as_posix()}|layername={layer_name}"
    layer = QgsVectorLayer(uri, f"step03_{layer_name}", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"La capa no pudo abrirse: {uri}")

    field_names = [field.name() for field in layer.fields()]
    request = QgsFeatureRequest().setLimit(limit)
    sample = []
    for feature in layer.getFeatures(request):
        sample.append(
            {
                "id": int(feature.id()),
                "attributes": {
                    name: _json_value(feature[name]) for name in field_names
                },
            }
        )

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "provider": layer.providerType(),
        "layer_name": layer_name,
        "path": str(path),
        "requested_limit": limit,
        "returned_count": len(sample),
        "fields": field_names,
        "sample": sample,
        "selected_feature_ids": [],
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\\archivo.gpkg').")
