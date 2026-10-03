"""Read-only inventory for the GeoPortIA QGIS reference packages."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "qgis_preflight"
OUT.mkdir(parents=True, exist_ok=True)

PACKAGES = [
    ("national", ROOT / "nal-QGis" / "QGis" / "MapaBaseMultiescala.gpkg", ROOT / "nal-QGis" / "QGis" / "MapaBaseMultiescala.qgz"),
    ("coahuila", ROOT / "coah-QGis" / "Coahuila_de_Zaragoza" / "mapa_base.gpkg", ROOT / "coah-QGis" / "Coahuila_de_Zaragoza" / "Coahuila_de_Zaragoza.qgz"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def qgis_text(element: ET.Element | None, name: str, default: str = "") -> str:
    if element is None:
        return default
    child = element.find(name)
    return (child.text or default).strip() if child is not None else default


def inspect_gpkg(package: str, path: Path) -> tuple[list[dict], list[dict], dict, dict]:
    layer_rows: list[dict] = []
    schema_rows: list[dict] = []
    discovery: dict = {"package": package, "matches": []}
    metadata: dict = {"package": package, "path": str(path), "tables": [], "contents": [], "geometry_columns": [], "spatial_ref_sys": [], "discovery": discovery, "integrity_check": "NOT_RUN"}
    uri = f"file:{path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as db:
        db.row_factory = sqlite3.Row
        crs_names = {row["srs_id"]: row["srs_name"] for row in db.execute("SELECT srs_id, srs_name FROM gpkg_spatial_ref_sys")}
        metadata["integrity_check"] = db.execute("PRAGMA integrity_check").fetchone()[0]
        for row in db.execute("SELECT * FROM gpkg_contents ORDER BY table_name"):
            content = dict(row)
            metadata["contents"].append(content)
            table = content["table_name"]
            count = None
            fields = []
            pk = ""
            if content["data_type"] == "features":
                count = db.execute(f' SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                fields = [dict(item) for item in db.execute(f'PRAGMA table_info("{table}")')]
                pk = next((item["name"] for item in fields if item["pk"]), "")
                for field in fields:
                    example = db.execute(f'SELECT "{field["name"]}" FROM "{table}" WHERE "{field["name"]}" IS NOT NULL LIMIT 1').fetchone()
                    schema_rows.append({"package": package, "layer_name": content.get("identifier") or table, "table_name": table, "field_name": field["name"], "field_type": field["type"], "nullable": not bool(field["notnull"]), "example_value": "" if example is None else str(example[0])[:200]})
                geom = db.execute("SELECT * FROM gpkg_geometry_columns WHERE table_name = ?", (table,)).fetchone()
                geom = dict(geom) if geom else {}
                spatial_index = bool(db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name LIKE ? LIMIT 1", (f'rtree_{table}_%',)).fetchone())
                layer_rows.append({"package": package, "layer_name": content.get("identifier") or table, "table_name": table, "geometry_type": geom.get("geometry_type_name", ""), "feature_count": count, "crs_authid": f"EPSG:{geom.get('srs_id')}" if geom.get("srs_id") is not None else "", "crs_name": crs_names.get(geom.get("srs_id"), ""), "epsg_if_available": geom.get("srs_id", ""), "extent_min_x": content.get("min_x", ""), "extent_min_y": content.get("min_y", ""), "extent_max_x": content.get("max_x", ""), "extent_max_y": content.get("max_y", ""), "field_count": len(fields), "primary_key": pk, "spatial_index_presence": spatial_index, "status": "INSPECTED"})
                text_fields = [field["name"] for field in fields if any(token in (field["type"] or "").upper() for token in ("CHAR", "TEXT", "CLOB"))]
                for field in text_fields:
                    for term in ("Saltillo", "Coahuila", "05030"):
                        matches = db.execute(f'SELECT "{field}" FROM "{table}" WHERE lower(CAST("{field}" AS TEXT)) LIKE ? LIMIT 5', (f"%{term.lower()}%",)).fetchall()
                        for match in matches:
                            discovery["matches"].append({"table_name": table, "layer_name": content.get("identifier") or table, "field_name": field, "search_term": term, "value": match[0]})
            metadata["tables"].append({"table_name": table, "data_type": content["data_type"], "identifier": content.get("identifier"), "description": content.get("description")})
        metadata["geometry_columns"] = [dict(row) for row in db.execute("SELECT * FROM gpkg_geometry_columns")]
        metadata["spatial_ref_sys"] = [dict(row) for row in db.execute("SELECT srs_name, srs_id, organization, organization_coordsys_id FROM gpkg_spatial_ref_sys")]
    return layer_rows, schema_rows, metadata, discovery


def inspect_qgz(package: str, path: Path, gpkg_path: Path) -> tuple[list[dict], dict, list[dict], list[dict]]:
    layers: list[dict] = []
    layouts: list[dict] = []
    broken: list[dict] = []
    project = {"package": package, "path": str(path), "archive_members": [], "project_version": "", "project_crs": {}, "layer_tree": [], "referenced_layers": 0, "provider_types": [], "styles": [], "labeling": [], "map_themes": [], "layouts": [], "reports": [], "relations": [], "broken_references": []}
    with zipfile.ZipFile(path, "r") as archive:
        project["archive_members"] = archive.namelist()
        qgs_name = next((name for name in archive.namelist() if name.lower().endswith(".qgs")), None)
        if not qgs_name:
            return layers, project, layouts, broken
        root = ET.fromstring(archive.read(qgs_name))
    project["project_version"] = root.attrib.get("version", "")
    crs = root.find("projectCrs/spatialrefsys")
    if crs is not None:
        project["project_crs"] = {child.tag: (child.text or "") for child in crs}
    for maplayer in root.findall(".//maplayer"):
        layer_id = maplayer.attrib.get("id", "")
        name = qgis_text(maplayer, "layername")
        provider = qgis_text(maplayer, "provider")
        datasource = qgis_text(maplayer, "datasource")
        source_path = datasource
        if "|layername=" in source_path:
            source_path = source_path.split("|", 1)[0]
        if source_path and not Path(source_path).is_absolute():
            candidate = (path.parent / source_path).resolve()
            if not candidate.exists() and "map_base.gpkg" in source_path:
                candidate = gpkg_path
            if not candidate.exists():
                broken.append({"package": package, "layer_name": name, "layer_id": layer_id, "source": datasource, "reason": "Referenced datasource not found relative to QGZ", "status": "BROKEN_OR_UNRESOLVED"})
        layer = {"package": package, "layer_name": name, "layer_id": layer_id, "provider": provider, "source": datasource, "visible_default": "", "style_reference": "embedded-or-project-defined", "labeling": "yes" if maplayer.find("labeling") is not None else "no", "status": "INSPECTED"}
        layers.append(layer)
        project["provider_types"].append(provider)
        project["styles"].append({"layer_name": name, "embedded_style": maplayer.find("renderer-v2") is not None})
        project["labeling"].append({"layer_name": name, "configured": maplayer.find("labeling") is not None})
    project["referenced_layers"] = len(layers)
    for layout in root.findall(".//layoutManager/layout"):
        row = {"package": package, "layout_name": layout.attrib.get("name", ""), "layout_type": "layout", "page_size": "", "orientation": "", "status": "INSPECTED"}
        layouts.append(row)
    project["layouts"] = layouts
    project["broken_references"] = broken
    return layers, project, layouts, broken


def main() -> None:
    inventory = []
    all_layers, all_schema, all_metadata, all_qgz_layers, all_qgz_projects, all_layouts, all_broken = [], [], [], [], [], [], []
    discoveries = []
    for package, gpkg, qgz in PACKAGES:
        for path, kind in ((gpkg, "gpkg"), (qgz, "qgz")):
            stat = path.stat()
            inventory.append({"package": package, "filename": path.name, "path": str(path), "extension": path.suffix, "size_bytes": stat.st_size, "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(), "sha256": sha256(path), "source": "INEGI — Mapa Base Multiescala — Estados Unidos Mexicanos" if package == "national" else "INEGI — Mapa Base — Coahuila de Zaragoza", "status": "FOUND"})
        layers, schema, metadata, discovery = inspect_gpkg(package, gpkg)
        qgz_layers, qgz_project, layouts, broken = inspect_qgz(package, qgz, gpkg)
        all_layers.extend(layers); all_schema.extend(schema); all_metadata.append(metadata); discoveries.append(discovery); all_qgz_layers.extend(qgz_layers); all_qgz_projects.append(qgz_project); all_layouts.extend(layouts); all_broken.extend(broken)
    write_csv(OUT / "file_inventory.csv", inventory, ["package", "filename", "path", "extension", "size_bytes", "modified_time", "sha256", "source", "status"])
    (OUT / "file_inventory.json").write_text(json.dumps({"execution_id":"GEO-QGIS-PREFLIGHT-001","repository":"RobertoGarciaITS/GeoPortIA-mx","status":"PASS","files":inventory,"search_roots":[str(ROOT / "nal-QGis"),str(ROOT / "coah-QGis")]}, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(OUT / "gpkg_layers.csv", all_layers, list(all_layers[0].keys()) if all_layers else ["package", "layer_name"])
    write_csv(OUT / "gpkg_schema.csv", all_schema, ["package", "layer_name", "table_name", "field_name", "field_type", "nullable", "example_value"])
    (OUT / "gpkg_metadata.json").write_text(json.dumps(all_metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(OUT / "qgz_layers.csv", all_qgz_layers, ["package", "layer_name", "layer_id", "provider", "source", "visible_default", "style_reference", "labeling", "status"])
    (OUT / "qgz_project.json").write_text(json.dumps(all_qgz_projects, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(OUT / "qgz_layouts.csv", all_layouts, ["package", "layout_name", "layout_type", "page_size", "orientation", "status"])
    write_csv(OUT / "broken_layers.csv", all_broken, ["package", "layer_name", "layer_id", "source", "reason", "status"])
    (OUT / "municipality_discovery.json").write_text(json.dumps(discoveries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"files": len(inventory), "spatial_layers": len(all_layers), "schema_fields": len(all_schema), "qgz_layers": len(all_qgz_layers), "layouts": len(all_layouts), "broken_references": len(all_broken), "discovery_matches": sum(len(item["matches"]) for item in discoveries)}, indent=2))


if __name__ == "__main__":
    main()
