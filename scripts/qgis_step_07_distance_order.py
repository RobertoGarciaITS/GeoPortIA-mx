"""QGIS step 07: calculate and order distances from the Saltillo point."""

from __future__ import annotations

from pathlib import Path


def run(
    gpkg_path: str,
    target_layer_name: str = "municipios",
    radius_m: float = 10000.0,
) -> dict:
    """Return radius matches ordered by planar distance in layer units."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsFeatureRequest, QgsVectorLayer
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")
    if not isinstance(radius_m, (int, float)) or radius_m <= 0:
        raise ValueError("radius_m debe ser un número mayor que cero")

    path = Path(gpkg_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {path}")

    source_layer = QgsVectorLayer(f"{path.as_posix()}|layername=municipios", "step07_source", "ogr")
    if not source_layer.isValid():
        raise RuntimeError("No pudo abrirse la capa municipal fuente.")

    source_request = QgsFeatureRequest().setFilterExpression(
        '"cve_ent" = \'05\' AND "cve_mun" = \'030\' AND "nomgeo" = \'Saltillo\''
    ).setLimit(1)
    saltillo = next(source_layer.getFeatures(source_request), None)
    if saltillo is None or saltillo.geometry().isEmpty():
        raise RuntimeError("No se encontró la geometría de Saltillo.")

    target_layer = QgsVectorLayer(
        f"{path.as_posix()}|layername={target_layer_name}", "step07_target", "ogr"
    )
    if not target_layer.isValid():
        raise RuntimeError(f"No pudo abrirse la capa objetivo: {target_layer_name}")
    if source_layer.crs() != target_layer.crs():
        raise RuntimeError("La capa fuente y la capa objetivo tienen CRS distintos.")

    request = QgsFeatureRequest().setDistanceWithin(saltillo.geometry(), float(radius_m))
    ordered = []
    for feature in target_layer.getFeatures(request):
        distance_m = saltillo.geometry().distance(feature.geometry())
        ordered.append({"feature_id": int(feature.id()), "distance_m": float(distance_m)})
    ordered.sort(key=lambda item: (item["distance_m"], item["feature_id"]))

    if any(item["distance_m"] > radius_m for item in ordered):
        raise RuntimeError("La consulta devolvió una entidad fuera del radio solicitado.")
    if ordered != sorted(ordered, key=lambda item: (item["distance_m"], item["feature_id"])):
        raise RuntimeError("Los resultados no quedaron ordenados por distancia.")

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
        "distance_method": "QgsGeometry.distance (projected CRS units)",
        "ordered_matches": ordered,
        "project_selection_changed": False,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\\archivo.gpkg').")
