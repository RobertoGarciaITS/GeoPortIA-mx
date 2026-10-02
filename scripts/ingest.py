"""Load the 10-record fixture into BigQuery with real GEOGRAPHY values."""
import os
from pathlib import Path
from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
PROJECT = os.environ["BIGQUERY_PROJECT"]
DATASET = os.environ.get("BIGQUERY_DATASET", "geoopportunity")
client = bigquery.Client(project=PROJECT)
table = f"{PROJECT}.{DATASET}.businesses"
rows = []
import csv
with (ROOT / "data/sample/businesses_10.csv").open(encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        row["latitude"] = float(row["latitude"]); row["longitude"] = float(row["longitude"])
        row["geography"] = f"POINT({row['longitude']} {row['latitude']})"
        rows.append(row)
errors = client.insert_rows_json(table, rows)
if errors: raise SystemExit(errors)
print(f"Loaded {len(rows)} businesses into {table}")
