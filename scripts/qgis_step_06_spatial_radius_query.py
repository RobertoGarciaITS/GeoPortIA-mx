"""QGIS step 06: query features within a radius of the Saltillo reference point.

This first version returns matching IDs without changing a QGIS project
selection. It is reusable for a future business layer by changing the target
layer name and radius.
"""

from __future__ import annotations

from pathlib import Path


def run(
    gpkg_path: str,
    target_layer_name: str = "municipios",
    radius_m: float = 10000.0,
) -> dict:
    """Return target features whose geometry is within ``radius_m`` metres."""
    try:
        from qgis.core import (
            Qgis,
            QgsApplication,
            QgsFeatureRequest,
            QgsVectorLayer,
        )
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")
    if not isinstance(radius_m, (int, float)) or radius_m <= 0:
        raise ValueError("radius_m debe ser un número mayor que cero")

    path = Path(gpkg_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {path}")

    source_uri = f"{path.as_posix()}|layername=municipios"
    source_layer = QgsVectorLayer(source_uri, "step06_source", "ogr")
    if not source_layer.isValid():
        raise RuntimeError(f"No pudo abrirse la capa fuente: {source_uri}")

    source_request = QgsFeatureRequest().setFilterExpression(
        '"cve_ent" = \'05\' AND "cve_mun" = \'030\' AND "nomgeo" = \'Saltillo\''
    ).setLimit(1)
    saltillo = next(source_layer.getFeatures(source_request), None)
    if saltillo is None or saltillo.geometry().isEmpty():
        raise RuntimeError("No se encontró la geometría de Saltillo.")

    target_uri = f"{path.as_posix()}|layername={target_layer_name}"
    target_layer = QgsVectorLayer(target_uri, "step06_target", "ogr")
    if not target_layer.isValid():
        raise RuntimeError(f"No pudo abrirse la capa objetivo: {target_uri}")
    if source_layer.crs() != target_layer.crs():
        raise RuntimeError("La capa fuente y la capa objetivo tienen CRS distintos.")

    request = QgsFeatureRequest().setDistanceWithin(saltillo.geometry(), float(radius_m))
    matches = [int(feature.id()) for feature in target_layer.getFeatures(request)]

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "provider": target_layer.providerType(),
        "source_layer": "municipios",
        "target_layer": target_layer_name,
        "path": str(path),
        "reference_feature_id": int(saltillo.id()),
        "radius_m": float(radius_m),
        "crs_authid": target_layer.crs().authid(),
        "matched_count": len(matches),
        "matched_feature_ids": matches,
        "project_selection_changed": False,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\\archivo.gpkg').")
