"""Build a structured QGIS project for Coahuila MG 2025."""

from __future__ import annotations

from pathlib import Path


def run(state_dir: str, output_project: str | None = None) -> dict:
    """Create a new QGZ project from the extracted Coahuila SHP layers."""
    try:
        from qgis.PyQt.QtCore import Qt
        from qgis.PyQt.QtGui import QColor
        from qgis.core import (
            Qgis,
            QgsFillSymbol,
            QgsLineSymbol,
            QgsPalLayerSettings,
            QgsProject,
            QgsSingleSymbolRenderer,
            QgsTextFormat,
            QgsCoordinateReferenceSystem,
            QgsUnitTypes,
            QgsVectorLayer,
            QgsVectorLayerSimpleLabeling,
        )
    except ImportError as exc:
        raise RuntimeError("PyQGIS no está disponible. Ejecuta este script desde QGIS.") from exc

    root = Path(state_dir).expanduser().resolve()
    data_dir = root / "conjunto_de_datos"
    if not data_dir.is_dir():
        raise FileNotFoundError(f"No existe conjunto_de_datos: {data_dir}")

    project_path = (
        Path(output_project).expanduser().resolve()
        if output_project
        else root / "Coahuila_MG_2025.qgz"
    )
    project_path.parent.mkdir(parents=True, exist_ok=True)

    project = QgsProject.instance()
    project.clear()
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:6372"))

    groups = {
        "base": project.layerTreeRoot().addGroup("01 - Base estatal y municipal"),
        "settlements": project.layerTreeRoot().addGroup("02 - Localidades"),
        "geo": project.layerTreeRoot().addGroup("03 - Marco geoestadístico"),
        "roads": project.layerTreeRoot().addGroup("04 - Vialidades"),
        "services": project.layerTreeRoot().addGroup("05 - Servicios e información complementaria"),
    }

    definitions = [
        ("05ent", "Coahuila - límite estatal", "base", True),
        ("05mun", "Municipios", "base", True),
        ("05l", "Localidades amanzanadas", "settlements", True),
        ("05lpr", "Localidades rurales puntuales", "settlements", False),
        ("05a", "AGEB urbanas", "geo", False),
        ("05ar", "AGEB rurales", "geo", False),
        ("05m", "Manzanas", "geo", False),
        ("05pe", "Polígonos externos", "geo", False),
        ("05pem", "Polígonos externos de manzana", "geo", False),
        ("05e", "Ejes de vialidad", "roads", False),
        ("05fm", "Frentes de manzana", "roads", False),
        ("05sia", "Servicios de área", "services", False),
        ("05sil", "Servicios lineales", "services", False),
        ("05sip", "Servicios puntuales", "services", False),
        ("05cd", "Caserío disperso", "services", False),
    ]

    added = []
    for stem, title, group_key, visible in definitions:
        shp_path = data_dir / f"{stem}.shp"
        if not shp_path.is_file():
            continue
        layer = QgsVectorLayer(str(shp_path), title, "ogr")
        if not layer.isValid():
            raise RuntimeError(f"No se pudo abrir {shp_path}")

        layer.setCrs(QgsCoordinateReferenceSystem("EPSG:6372"))
        if stem == "05ent":
            symbol = QgsFillSymbol.createSimple({
                "color": "#ffffff00",
                "outline_color": "#555555",
                "outline_width": "0.8",
                "outline_width_unit": "MM",
            })
            symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
            layer.setRenderer(QgsSingleSymbolRenderer(symbol))
        elif stem == "05mun":
            symbol = QgsFillSymbol.createSimple({
                "color": "#ffffff00",
                "outline_color": "#AAAAAA",
                "outline_width": "0.35",
                "outline_width_unit": "Point",
            })
            symbol.symbolLayer(0).setBrushStyle(Qt.BrushStyle.NoBrush)
            layer.setRenderer(QgsSingleSymbolRenderer(symbol))
        elif layer.geometryType() == Qgis.GeometryType.Line:
            layer.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple({
                "color": "#B8B8B8",
                "width": "0.2",
                "width_unit": "MM",
            })))

        if stem == "05mun":
            label = QgsPalLayerSettings()
            label.fieldName = "NOMGEO"
            text = QgsTextFormat()
            text.setFont(QgsTextFormat().font())
            text.setSize(9)
            text.setSizeUnit(QgsUnitTypes.RenderPoints)
            text.setColor(QColor("#444444"))
            label.setFormat(text)
            layer.setLabeling(QgsVectorLayerSimpleLabeling(label))
            layer.setLabelsEnabled(True)

        project.addMapLayer(layer, False)
        groups[group_key].addLayer(layer)
        groups[group_key].findLayer(layer.id()).setItemVisibilityChecked(visible)
        added.append({
            "file": shp_path.name,
            "name": title,
            "visible": visible,
            "feature_count": int(layer.featureCount()),
            "geometry_type": layer.geometryType().name,
        })

    if not project.write(str(project_path)):
        raise RuntimeError(f"No se pudo guardar el proyecto: {project_path}")

    return {
        "status": "PASS",
        "qgis_version": Qgis.QGIS_VERSION,
        "project": str(project_path),
        "crs_authid": "EPSG:6372",
        "layer_count": len(added),
        "layers": added,
        "modified_source": False,
    }


if __name__ == "__main__":
    raise SystemExit("Ejecuta este archivo desde la consola Python de QGIS y llama run(r'RUTA_ESTADO').")
