from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

try:
    from google.cloud import bigquery
except ImportError:  # Local fixture mode does not require the cloud SDK.
    bigquery = None

from app.models.schemas import Business, Municipality

ROOT = Path(__file__).resolve().parents[4]
CSV_PATH = ROOT / "data" / "sample" / "businesses_10.csv"
MUNICIPALITY_PATH = ROOT / "data" / "sample" / "municipality_saltillo.geojson"


def _fixture_businesses() -> list[Business]:
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        result = []
        for row in csv.DictReader(handle):
            row["latitude"] = float(row["latitude"])
            row["longitude"] = float(row["longitude"])
            result.append(Business(**row))
        return result


def _bigquery_client() -> bigquery.Client | None:
    if os.getenv("GEOOPPORTUNITY_USE_BIGQUERY") != "1":
        return None
    project = os.getenv("BIGQUERY_PROJECT")
    dataset = os.getenv("BIGQUERY_DATASET")
    if not project or not dataset:
        raise RuntimeError("BIGQUERY_PROJECT and BIGQUERY_DATASET are required when GEOOPPORTUNITY_USE_BIGQUERY=1")
    if bigquery is None:
        raise RuntimeError("BigQuery SDK is not installed; install apps/api/requirements.txt")
    return bigquery.Client(project=project)


def businesses() -> list[Business]:
    client = _bigquery_client()
    if not client:
        return _fixture_businesses()
    dataset = os.environ["BIGQUERY_DATASET"]
    query = f"""
        SELECT business_id, source_record_id, name, scian, economic_activity,
               employee_range, latitude, longitude, municipality_id, source,
               ST_ASGEOJSON(geography) AS geography
        FROM `{client.project}.{dataset}.businesses`
        ORDER BY business_id
    """
    return [Business(**dict(row), geography=json.loads(row["geography"])) for row in client.query(query).result()]


def municipality() -> Municipality:
    with MUNICIPALITY_PATH.open(encoding="utf-8") as handle:
        geometry = json.load(handle)
    return Municipality(
        municipality_id="MEX-COA-SALTILLO",
        cvegeo="05030",
        municipality_name="Saltillo",
        state_name="Coahuila de Zaragoza",
        source="INEGI. Marco Geoestadístico, diciembre de 2025",
        geometry=geometry,
    )


def distance_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def nearby(lat: float, lng: float, radius_m: float) -> list[Business]:
    client = _bigquery_client()
    if client:
        dataset = os.environ["BIGQUERY_DATASET"]
        query = f"""
            SELECT business_id, source_record_id, name, scian, economic_activity,
                   employee_range, latitude, longitude, municipality_id, source,
                   ST_ASGEOJSON(geography) AS geography
            FROM `{client.project}.{dataset}.businesses`
            WHERE ST_DWITHIN(geography, ST_GEOGPOINT(@lng, @lat), @radius_m)
            ORDER BY business_id
        """
        config = bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter("lng", "FLOAT64", lng),
            bigquery.ScalarQueryParameter("lat", "FLOAT64", lat),
            bigquery.ScalarQueryParameter("radius_m", "FLOAT64", radius_m),
        ])
        return [Business(**dict(row), geography=json.loads(row["geography"])) for row in client.query(query, job_config=config).result()]
    return [b for b in _fixture_businesses() if distance_m(lat, lng, b.latitude, b.longitude) <= radius_m]
