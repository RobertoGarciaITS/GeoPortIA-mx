"""Export Saltillo as an outline-only PDF with a white background."""

from __future__ import annotations

from pathlib import Path


def run(gpkg_path: str, output_path: str) -> dict:
    """Render Saltillo without fill color and save it as a PDF."""
    try:
        from qgis.PyQt.QtCore import QSize, Qt
        from qgis.PyQt.QtGui import QColor, QPageLayout, QPageSize, QPainter, QPdfWriter
        from qgis.core import (
            Qgis,
            QgsApplication,
            QgsMapRendererCustomPainterJob,
            QgsMapSettings,
            QgsSingleSymbolRenderer,
            QgsFillSymbol,
            QgsVectorLayer,
        )
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")

    source_path = Path(gpkg_path).expanduser().resolve()
    export_path = Path(output_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"No existe el GeoPackage: {source_path}")
    if export_path.suffix.lower() != ".pdf":
        raise ValueError("La salida debe tener extensión .pdf")
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

    outline_symbol = QgsFillSymbol.createSimple(
        {
            "color": "#ffffff",
            "outline_color": "#AAAAAA",
            "outline_width": "0.35",
            "outline_width_unit": "Point",
        }
    )
    symbol_layer = outline_symbol.symbolLayer(0)
    symbol_layer.setBrushStyle(Qt.BrushStyle.NoBrush)
    layer.setRenderer(QgsSingleSymbolRenderer(outline_symbol))

    settings = QgsMapSettings()
    settings.setLayers([layer])
    settings.setDestinationCrs(layer.crs())
    settings.setExtent(extent)
    settings.setOutputSize(QSize(1123, 794))
    settings.setOutputDpi(150)
    settings.setBackgroundColor(QColor("#ffffff"))

    export_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = QPdfWriter(str(export_path))
    pdf.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    pdf.setPageOrientation(QPageLayout.Orientation.Landscape)
    pdf.setResolution(150)
    painter = QPainter(pdf)
    job = QgsMapRendererCustomPainterJob(settings, painter)
    job.renderSynchronously()
    painter.end()

    if not export_path.is_file() or export_path.stat().st_size == 0:
        raise RuntimeError(f"No se pudo crear el PDF: {export_path}")

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "source_path": str(source_path),
        "output_path": str(export_path),
        "format": "pdf",
        "page": "A4 landscape",
        "fill": "transparent",
        "outline": "#AAAAAA, 0.35 Point",
        "crs_authid": layer.crs().authid(),
        "feature_count": 1,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'FUENTE', r'SALIDA.pdf').")
