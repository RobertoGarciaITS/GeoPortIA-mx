"""QGIS step 05: create an in-memory reference point inside Saltillo."""

from __future__ import annotations

from pathlib import Path


def run(gpkg_path: str, layer_name: str = "municipios") -> dict:
    """Find Saltillo and derive a temporary point guaranteed inside it."""
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
    layer = QgsVectorLayer(uri, f"step05_{layer_name}", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"La capa no pudo abrirse: {uri}")

    expression = '"cve_ent" = \'05\' AND "cve_mun" = \'030\' AND "nomgeo" = \'Saltillo\''
    request = QgsFeatureRequest().setFilterExpression(expression).setLimit(1)
    feature = next(layer.getFeatures(request), None)
    if feature is None or feature.geometry().isEmpty():
        raise RuntimeError("No se encontró una geometría válida para Saltillo.")

    source_geometry = feature.geometry()
    reference_point = source_geometry.pointOnSurface()
    if reference_point.isEmpty() or not source_geometry.contains(reference_point):
        raise RuntimeError("El punto de referencia no quedó dentro de Saltillo.")
    point_xy = reference_point.asPoint()

    crs = layer.crs()
    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "provider": layer.providerType(),
        "layer_name": layer_name,
        "path": str(path),
        "source_feature_id": int(feature.id()),
        "municipality": "Saltillo",
        "method": "pointOnSurface",
        "point": {
            "x": point_xy.x(),
            "y": point_xy.y(),
            "crs_authid": crs.authid(),
        },
        "point_inside_source": True,
        "temporary_only": True,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\\archivo.gpkg').")
