"""Export a simple Saltillo map image with headless PyQGIS."""

from __future__ import annotations

from pathlib import Path


def run(
    gpkg_path: str,
    output_path: str,
    width: int = 1600,
    height: int = 1200,
) -> dict:
    """Render Saltillo to PNG without changing the source GeoPackage."""
    try:
        from qgis.PyQt.QtCore import QSize
        from qgis.PyQt.QtGui import QColor, QImage, QPainter
        from qgis.core import (
            Qgis,
            QgsApplication,
            QgsFillSymbol,
            QgsMapRendererCustomPainterJob,
            QgsMapSettings,
            QgsSingleSymbolRenderer,
            QgsVectorLayer,
        )
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")
    if width < 400 or height < 300:
        raise ValueError("El tamaño mínimo es 400x300 píxeles")

    source_path = Path(gpkg_path).expanduser().resolve()
    export_path = Path(output_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {source_path}")
    if export_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("La salida debe ser PNG o JPEG")
    if export_path == source_path:
        raise ValueError("La salida no puede sobrescribir el GeoPackage")

    layer = QgsVectorLayer(f"{source_path.as_posix()}|layername=municipios", "Saltillo", "ogr")
    if not layer.isValid():
        raise RuntimeError("No pudo abrirse la capa municipios.")

    saltillo_filter = '"cve_ent" = \'05\' AND "cve_mun" = \'030\' AND "nomgeo" = \'Saltillo\''
    layer.setSubsetString(saltillo_filter)
    if layer.featureCount() != 1:
        raise RuntimeError(f"Se esperaba una entidad Saltillo; se encontraron {layer.featureCount()}.")

    extent = layer.extent()
    margin_x = max(extent.width() * 0.08, 1000.0)
    margin_y = max(extent.height() * 0.08, 1000.0)
    extent.setXMinimum(extent.xMinimum() - margin_x)
    extent.setXMaximum(extent.xMaximum() + margin_x)
    extent.setYMinimum(extent.yMinimum() - margin_y)
    extent.setYMaximum(extent.yMaximum() + margin_y)

    symbol = QgsFillSymbol.createSimple(
        {
            "color": "#2f80ed",
            "outline_color": "#123b68",
            "outline_width": "0.8",
        }
    )
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))

    settings = QgsMapSettings()
    settings.setLayers([layer])
    settings.setDestinationCrs(layer.crs())
    settings.setExtent(extent)
    settings.setOutputSize(QSize(width, height))
    settings.setOutputDpi(150)
    settings.setBackgroundColor(QColor("#f7f9fc"))

    export_path.parent.mkdir(parents=True, exist_ok=True)
    image = QImage(width, height, QImage.Format.Format_ARGB32)
    image.fill(QColor("#f7f9fc"))
    painter = QPainter(image)
    job = QgsMapRendererCustomPainterJob(settings, painter)
    job.renderSynchronously()
    painter.end()
    if not image.save(str(export_path)):
        raise RuntimeError(f"No se pudo guardar la imagen: {export_path}")

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "source_path": str(source_path),
        "output_path": str(export_path),
        "format": export_path.suffix.lower().lstrip("."),
        "width": width,
        "height": height,
        "crs_authid": layer.crs().authid(),
        "feature_count": 1,
        "filter": saltillo_filter,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'FUENTE', r'SALIDA.png').")
