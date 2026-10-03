"""QGIS step 02: read vector-layer metadata without iterating features.

Run this inside the QGIS Python Console after step 01 passes. The source is
opened read-only and no feature iterator, edit session, export, or project
write is performed.
"""

from __future__ import annotations

from pathlib import Path


def run(gpkg_path: str, layer_name: str = "municipios") -> dict:
    """Read stable metadata from a GeoPackage vector layer."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsVectorLayer, QgsWkbTypes
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")

    path = Path(gpkg_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {path}")
    if path.suffix.lower() != ".gpkg":
        raise ValueError(f"El archivo no tiene extensión .gpkg: {path}")

    uri = f"{path.as_posix()}|layername={layer_name}"
    layer = QgsVectorLayer(uri, f"step02_{layer_name}", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"La capa no pudo abrirse: {uri}")

    crs = layer.crs()
    extent = layer.extent()
    geometry_name = QgsWkbTypes.geometryDisplayString(layer.geometryType())
    fields = [field.name() for field in layer.fields()]

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "provider": layer.providerType(),
        "layer_name": layer_name,
        "path": str(path),
        "valid": layer.isValid(),
        "geometry_type": geometry_name,
        "wkb_type": int(layer.wkbType()),
        "crs_authid": crs.authid(),
        "crs_description": crs.description(),
        "field_count": len(fields),
        "fields": fields,
        "extent": {
            "xmin": extent.xMinimum(),
            "ymin": extent.yMinimum(),
            "xmax": extent.xMaximum(),
            "ymax": extent.yMaximum(),
        },
        "iterated_features": False,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\\archivo.gpkg').")
