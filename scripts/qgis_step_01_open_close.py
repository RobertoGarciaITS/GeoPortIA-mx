"""QGIS step 01: verify PyQGIS, open a GeoPackage layer, and release it.

Run this inside the QGIS Python Console. It intentionally does not iterate
features, export data, modify the project, or write to the GeoPackage.
"""

from __future__ import annotations

import gc
from pathlib import Path


def run(gpkg_path: str, layer_name: str = "municipios") -> dict:
    """Run the read-only connection/open/close smoke test."""
    try:
        from qgis.core import Qgis, QgsApplication, QgsProviderRegistry, QgsVectorLayer
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde la consola Python de QGIS.") from exc

    app = QgsApplication.instance()
    if app is None:
        raise RuntimeError("No existe una instancia activa de QGIS. Abre QGIS antes de ejecutar el script.")

    path = Path(gpkg_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {path}")
    if path.suffix.lower() != ".gpkg":
        raise ValueError(f"El archivo no tiene extensión .gpkg: {path}")

    provider_registry = QgsProviderRegistry.instance()
    ogr_metadata = provider_registry.providerMetadata("ogr")
    if ogr_metadata is None:
        raise RuntimeError("El proveedor OGR no está disponible en esta instalación de QGIS.")

    uri = f"{path.as_posix()}|layername={layer_name}"
    layer = QgsVectorLayer(uri, f"step01_{layer_name}", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"La capa no pudo abrirse: {uri}")

    result = {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "provider": layer.providerType(),
        "layer_name": layer_name,
        "path": str(path),
        "opened": True,
        "read_features": False,
        "modified_source": False,
    }

    # QgsVectorLayer has no public close() method. Releasing the Python
    # reference and collecting garbage closes the provider handle without
    # saving or changing the source dataset.
    layer = None
    gc.collect()
    result["released"] = True
    return result


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA\archivo.gpkg').")
