"""QGIS step 08: export radius results to a CSV outside the GeoPackage."""

from __future__ import annotations

import csv
from pathlib import Path


def run(
    gpkg_path: str,
    output_path: str,
    target_layer_name: str = "municipios",
    radius_m: float = 10000.0,
) -> dict:
    """Calculate radius matches and export a small tabular result."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsFeatureRequest, QgsVectorLayer
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")
    if radius_m <= 0:
        raise ValueError("radius_m debe ser mayor que cero")

    source_path = Path(gpkg_path).expanduser().resolve()
    export_path = Path(output_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {source_path}")
    if export_path == source_path or export_path.suffix.lower() == ".gpkg":
        raise ValueError("La salida debe estar fuera del GeoPackage y no puede ser .gpkg")

    source_layer = QgsVectorLayer(f"{source_path.as_posix()}|layername=municipios", "step08_source", "ogr")
    target_layer = QgsVectorLayer(
        f"{source_path.as_posix()}|layername={target_layer_name}", "step08_target", "ogr"
    )
    if not source_layer.isValid() or not target_layer.isValid():
        raise RuntimeError("No pudo abrirse la capa fuente u objetivo.")
    if source_layer.crs() != target_layer.crs():
        raise RuntimeError("La capa fuente y la capa objetivo tienen CRS distintos.")

    source_request = QgsFeatureRequest().setFilterExpression(
        '"cve_ent" = \'05\' AND "cve_mun" = \'030\' AND "nomgeo" = \'Saltillo\''
    ).setLimit(1)
    saltillo = next(source_layer.getFeatures(source_request), None)
    if saltillo is None:
        raise RuntimeError("No se encontró Saltillo.")

    request = QgsFeatureRequest().setDistanceWithin(saltillo.geometry(), float(radius_m))
    rows = []
    for feature in target_layer.getFeatures(request):
        rows.append(
            {
                "feature_id": int(feature.id()),
                "nomgeo": str(feature["nomgeo"]) if "nomgeo" in feature.fields().names() else "",
                "cve_ent": str(feature["cve_ent"]) if "cve_ent" in feature.fields().names() else "",
                "cve_mun": str(feature["cve_mun"]) if "cve_mun" in feature.fields().names() else "",
                "distance_m": float(saltillo.geometry().distance(feature.geometry())),
            }
        )
    rows.sort(key=lambda row: (row["distance_m"], row["feature_id"]))

    export_path.parent.mkdir(parents=True, exist_ok=True)
    with export_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature_id", "nomgeo", "cve_ent", "cve_mun", "distance_m"])
        writer.writeheader()
        writer.writerows(rows)

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "target_layer": target_layer_name,
        "source_path": str(source_path),
        "output_path": str(export_path),
        "radius_m": float(radius_m),
        "export_format": "CSV UTF-8 with BOM",
        "exported_count": len(rows),
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'FUENTE', r'SALIDA.csv').")
