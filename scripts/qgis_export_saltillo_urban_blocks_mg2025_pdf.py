"""Export Saltillo urban area with its urban manzana/block boundaries."""

from __future__ import annotations

from pathlib import Path


def run(state_dir: str, output_path: str) -> dict:
    """Render urban localities and intersecting manzanas in memory."""
    try:
        from qgis.PyQt.QtCore import QSize, Qt
        from qgis.PyQt.QtGui import QColor, QPageLayout, QPageSize, QPainter, QPdfWriter
        from qgis.core import (
            Qgis,
            QgsApplication,
            QgsCoordinateReferenceSystem,
            QgsFeature,
            QgsFeatureRequest,
            QgsFillSymbol,
            QgsMapRendererCustomPainterJob,
            QgsMapSettings,
            QgsMemoryProviderUtils,
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
    data_dir = root / "conjunto_de_datos"
    locality_path = data_dir / "05l.shp"
    blocks_path = data_dir / "05m.shp"
    export_path = Path(output_path).expanduser().resolve()
    if not locality_path.is_file() or not blocks_path.is_file():
        raise FileNotFoundError("Faltan 05l.shp o 05m.shp en el paquete de Coahuila.")
    if export_path.suffix.lower() != ".pdf":
        raise ValueError("La salida debe tener extensión .pdf")

    crs = QgsCoordinateReferenceSystem("EPSG:6372")
    urban = QgsVectorLayer(str(locality_path), "Área urbana de Saltillo", "ogr")
    source_blocks = QgsVectorLayer(str(blocks_path), "Manzanas fuente", "ogr")
    if not urban.isValid() or not source_blocks.isValid():
        raise RuntimeError("No se pudieron abrir 05l.shp y 05m.shp.")
    urban.setCrs(crs)
    source_blocks.setCrs(crs)

    urban_filter = '"CVE_ENT" = \'05\' AND "CVE_MUN" = \'030\' AND "AMBITO" = \'Urbana\''
    urban.setSubsetString(urban_filter)
    urban_feature = next(urban.getFeatures(), None)
    if urban_feature is None or urban_feature.geometry().isEmpty():
        raise RuntimeError("No se encontró el área urbana de Saltillo.")
    urban_geometry = urban_feature.geometry()

    block_filter = '"CVE_ENT" = \'05\' AND "CVE_MUN" = \'030\''
    request = QgsFeatureRequest().setFilterExpression(block_filter)
    memory_blocks = QgsVectorLayer("Polygon?crs=EPSG:6372", "Manzanas urbanas", "memory")
    provider = memory_blocks.dataProvider()
    selected = []
    for source_feature in source_blocks.getFeatures(request):
        geometry = source_feature.geometry()
        if not geometry.isEmpty() and geometry.intersects(urban_geometry):
            feature = QgsFeature()
            feature.setGeometry(geometry)
            selected.append(feature)
    provider.addFeatures(selected)
    memory_blocks.updateExtents()
    if not selected:
        raise RuntimeError("No se encontraron manzanas dentro del área urbana.")

    urban_symbol = QgsFillSymbol.createSimple({
        "color": "#ffffff",
        "outline_color": "#AAAAAA",
        "outline_width": "0.35",
        "outline_width_unit": "Point",
    })
    urban_symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
    urban.setRenderer(QgsSingleSymbolRenderer(urban_symbol))

    block_symbol = QgsFillSymbol.createSimple({
        "color": "#ffffff",
        "outline_color": "#999999",
        "outline_width": "0.18",
        "outline_width_unit": "Point",
    })
    block_symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
    memory_blocks.setRenderer(QgsSingleSymbolRenderer(block_symbol))

    labels = QgsPalLayerSettings()
    labels.fieldName = "NOMGEO"
    label_format = QgsTextFormat()
    label_format.setSize(12)
    label_format.setSizeUnit(QgsUnitTypes.RenderPoints)
    label_format.setColor(QColor("#444444"))
    labels.setFormat(label_format)
    urban.setLabeling(QgsVectorLayerSimpleLabeling(labels))
    urban.setLabelsEnabled(True)

    extent = urban.extent()
    margin_x = max(extent.width() * 0.08, 1000.0)
    margin_y = max(extent.height() * 0.08, 1000.0)
    extent.setXMinimum(extent.xMinimum() - margin_x)
    extent.setXMaximum(extent.xMaximum() + margin_x)
    extent.setYMinimum(extent.yMinimum() - margin_y)
    extent.setYMaximum(extent.yMaximum() + margin_y)

    settings = QgsMapSettings()
    settings.setLayers([urban, memory_blocks])
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
        "source_localities": str(locality_path),
        "source_blocks": str(blocks_path),
        "output_path": str(export_path),
        "format": "pdf",
        "page": "A4 landscape",
        "urban_filter": urban_filter,
        "block_filter": block_filter,
        "urban_count": 1,
        "urban_block_count": len(selected),
        "urban_outline": "#AAAAAA, 0.35 Point",
        "block_outline": "#999999, 0.18 Point",
        "crs_authid": "EPSG:6372",
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA_ESTADO', r'SALIDA.pdf').")
