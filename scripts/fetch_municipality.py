"""Download and normalize an official INEGI municipality GeoJSON feature."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "source"
OUTPUT_PATH = ROOT / "data" / "sample" / "municipality_saltillo.geojson"
SOURCE_PATH = SOURCE_DIR / "municipality_saltillo_inegi_2025.json"
URL = "https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/05030"


def main() -> None:
    request = Request(URL, headers={"User-Agent": "GeoOpportunity-MX/0.1"})
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    features = payload.get("features", [])
    if len(features) != 1:
        raise ValueError(f"Expected exactly one INEGI feature for 05030, got {len(features)}")
    feature = features[0]
    properties = feature.get("properties", {})
    if properties.get("cvegeo") != "05030" or properties.get("nomgeo") != "Saltillo":
        raise ValueError("INEGI response is not the expected Saltillo municipality")
    geometry = feature.get("geometry")
    if not geometry or geometry.get("type") not in {"Polygon", "MultiPolygon"}:
        raise ValueError("INEGI response does not contain a polygon geometry")
    geometry = dict(geometry)
    # BigQuery GEOGRAPHY expects longitude/latitude WGS84 GeoJSON. The
    # service includes a CRS member; preserve it in the raw source only.
    geometry.pop("crs", None)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_PATH.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Saved official source: {SOURCE_PATH}")
    print(f"Saved normalized geometry: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
