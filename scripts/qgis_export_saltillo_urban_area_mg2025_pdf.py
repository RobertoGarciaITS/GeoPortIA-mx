"""Export only the urban locality area of Saltillo."""

from __future__ import annotations

from pathlib import Path


def run(state_dir: str, output_path: str) -> dict:
    """Render the Saltillo locality where AMBITO is Urbana."""
    try:
        from qgis.PyQt.QtCore import QSize, Qt
        from qgis.PyQt.QtGui import QColor, QPageLayout, QPageSize, QPainter, QPdfWriter
        from qgis.core import (
            Qgis,
            QgsApplication,
            QgsCoordinateReferenceSystem,
            QgsFillSymbol,
            QgsMapRendererCustomPainterJob,
            QgsMapSettings,
            QgsPalLayerSettings,
            QgsSingleSymbolRenderer,
            QgsTextFormat,
            QgsUnitTypes,
            QgsVectorLayer,
            QgsVectorLayerSimpleLabeling,
        )
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    if QgsApplication.instance() is None:
        raise RuntimeError("No existe una instancia activa de QGIS.")

    root = Path(state_dir).expanduser().resolve()
    source_path = root / "conjunto_de_datos" / "05l.shp"
    export_path = Path(output_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"No existe la capa de localidades: {source_path}")
    if export_path.suffix.lower() != ".pdf":
        raise ValueError("La salida debe tener extensión .pdf")

    layer = QgsVectorLayer(str(source_path), "Área urbana de Saltillo", "ogr")
    if not layer.isValid():
        raise RuntimeError("No pudo abrirse 05l.shp.")
    crs = QgsCoordinateReferenceSystem("EPSG:6372")
    layer.setCrs(crs)

    urban_filter = '"CVE_ENT" = \'05\' AND "CVE_MUN" = \'030\' AND "AMBITO" = \'Urbana\''
    layer.setSubsetString(urban_filter)
    if layer.featureCount() != 1:
        raise RuntimeError(f"Se esperaba un área urbana; se encontraron {layer.featureCount()}.")

    symbol = QgsFillSymbol.createSimple({
        "color": "#ffffff",
        "outline_color": "#AAAAAA",
        "outline_width": "0.35",
        "outline_width_unit": "Point",
    })
    symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))

    labels = QgsPalLayerSettings()
    labels.fieldName = "NOMGEO"
    label_format = QgsTextFormat()
    label_format.setSize(12)
    label_format.setSizeUnit(QgsUnitTypes.RenderPoints)
    label_format.setColor(QColor("#444444"))
    labels.setFormat(label_format)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
    layer.setLabelsEnabled(True)

    extent = layer.extent()
    margin_x = max(extent.width() * 0.10, 1000.0)
    margin_y = max(extent.height() * 0.10, 1000.0)
    extent.setXMinimum(extent.xMinimum() - margin_x)
    extent.setXMaximum(extent.xMaximum() + margin_x)
    extent.setYMinimum(extent.yMinimum() - margin_y)
    extent.setYMaximum(extent.yMaximum() + margin_y)

    settings = QgsMapSettings()
    settings.setLayers([layer])
    settings.setDestinationCrs(crs)
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
        "filter": urban_filter,
        "fill": "transparent / NoBrush",
        "outline": "#AAAAAA, 0.35 Point",
        "label": "NOMGEO",
        "urban_count": 1,
        "crs_authid": "EPSG:6372",
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA_ESTADO', r'SALIDA.pdf').")
