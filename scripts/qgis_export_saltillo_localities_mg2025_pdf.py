"""Export Saltillo with locality polygons and NOMGEO labels."""

from __future__ import annotations

from pathlib import Path


def run(state_dir: str, output_path: str) -> dict:
    """Render the Saltillo municipality and its locality polygons."""
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
    data_dir = root / "conjunto_de_datos"
    export_path = Path(output_path).expanduser().resolve()
    municipality_path = data_dir / "05mun.shp"
    locality_path = data_dir / "05l.shp"
    if not municipality_path.is_file() or not locality_path.is_file():
        raise FileNotFoundError("Faltan 05mun.shp o 05l.shp en el paquete de Coahuila.")
    if export_path.suffix.lower() != ".pdf":
        raise ValueError("La salida debe tener extensión .pdf")

    crs = QgsCoordinateReferenceSystem("EPSG:6372")
    municipality = QgsVectorLayer(str(municipality_path), "Saltillo", "ogr")
    localities = QgsVectorLayer(str(locality_path), "Localidades", "ogr")
    if not municipality.isValid() or not localities.isValid():
        raise RuntimeError("No se pudieron abrir las capas municipales o de localidades.")
    municipality.setCrs(crs)
    localities.setCrs(crs)

    municipality_filter = '"CVE_ENT" = \'05\' AND "CVE_MUN" = \'030\''
    municipality.setSubsetString(municipality_filter)
    localities.setSubsetString(municipality_filter)
    if municipality.featureCount() != 1:
        raise RuntimeError(f"Se esperaba un municipio; se encontraron {municipality.featureCount()}.")
    locality_count = localities.featureCount()
    if locality_count < 1:
        raise RuntimeError("No se encontraron localidades para Saltillo.")

    municipality_symbol = QgsFillSymbol.createSimple({
        "color": "#ffffff",
        "outline_color": "#AAAAAA",
        "outline_width": "0.35",
        "outline_width_unit": "Point",
    })
    municipality_symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
    municipality.setRenderer(QgsSingleSymbolRenderer(municipality_symbol))

    locality_symbol = QgsFillSymbol.createSimple({
        "color": "#ffffff",
        "outline_color": "#CCCCCC",
        "outline_width": "0.2",
        "outline_width_unit": "Point",
    })
    locality_symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
    localities.setRenderer(QgsSingleSymbolRenderer(locality_symbol))

    labels = QgsPalLayerSettings()
    labels.fieldName = "NOMGEO"
    label_format = QgsTextFormat()
    label_format.setSize(5.5)
    label_format.setSizeUnit(QgsUnitTypes.RenderPoints)
    label_format.setColor(QColor("#666666"))
    labels.setFormat(label_format)
    localities.setLabeling(QgsVectorLayerSimpleLabeling(labels))
    localities.setLabelsEnabled(True)

    extent = municipality.extent()
    margin_x = max(extent.width() * 0.08, 1000.0)
    margin_y = max(extent.height() * 0.08, 1000.0)
    extent.setXMinimum(extent.xMinimum() - margin_x)
    extent.setXMaximum(extent.xMaximum() + margin_x)
    extent.setYMinimum(extent.yMinimum() - margin_y)
    extent.setYMaximum(extent.yMaximum() + margin_y)

    settings = QgsMapSettings()
    settings.setLayers([municipality, localities])
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
        "source_municipalities": str(municipality_path),
        "source_localities": str(locality_path),
        "output_path": str(export_path),
        "format": "pdf",
        "page": "A4 landscape",
        "municipality_outline": "#AAAAAA, 0.35 Point",
        "locality_outline": "#CCCCCC, 0.2 Point",
        "locality_label_field": "NOMGEO",
        "locality_count": int(locality_count),
        "crs_authid": "EPSG:6372",
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA_ESTADO', r'SALIDA.pdf').")
