"""Inventory a Marco Geoestadístico state package with PyQGIS."""

from __future__ import annotations

from pathlib import Path


def run(state_dir: str) -> dict:
    """Inspect every SHP in a state package without editing or exporting."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsVectorLayer
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")

    root = Path(state_dir).expanduser().resolve()
    data_dir = root / "conjunto_de_datos"
    if not data_dir.is_dir():
        raise FileNotFoundError(f"No existe conjunto_de_datos: {data_dir}")

    layers = []
    for shp_path in sorted(data_dir.glob("*.shp")):
        layer = QgsVectorLayer(str(shp_path), shp_path.stem, "ogr")
        if not layer.isValid():
            raise RuntimeError(f"No se pudo abrir: {shp_path}")
        layers.append(
            {
                "file": shp_path.name,
                "layer_name": shp_path.stem,
                "provider": layer.providerType(),
                "geometry_type": layer.geometryType().name,
                "wkb_type": int(layer.wkbType()),
                "crs_authid": layer.crs().authid(),
                "feature_count": int(layer.featureCount()),
                "fields": [field.name() for field in layer.fields()],
                "extent": {
                    "xmin": layer.extent().xMinimum(),
                    "ymin": layer.extent().yMinimum(),
                    "xmax": layer.extent().xMaximum(),
                    "ymax": layer.extent().yMaximum(),
                },
            }
        )

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "state": "Coahuila de Zaragoza",
        "state_dir": str(root),
        "layer_count": len(layers),
        "layers": layers,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA_ESTADO').")
