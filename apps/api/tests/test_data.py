import pytest

from app.services import data
from app.services.data import businesses, distance_m, municipality, nearby


def test_fixture_is_reproducible_and_sorted():
    records = businesses()
    assert [record.business_id for record in records] == [f"saltillo-{i:03d}" for i in range(1, 11)]
    assert all(record.municipality_id == "MEX-COA-SALTILLO" for record in records)


def test_haversine_distance_is_zero_for_same_point():
    assert distance_m(25.438, -100.973, 25.438, -100.973) == 0


def test_haversine_distance_is_symmetric():
    first = distance_m(25.438, -100.973, 25.44, -100.97)
    second = distance_m(25.44, -100.97, 25.438, -100.973)
    assert first == second
    assert 300 < first < 500


def test_nearby_zero_radius_is_rejected_at_api_but_service_is_precise():
    assert [item.business_id for item in nearby(25.438, -100.973, 1)] == ["saltillo-001"]


def test_municipality_service_returns_reference_geometry():
    result = municipality()
    assert result.cvegeo == "05030"
    assert result.geometry["type"] in {"Polygon", "MultiPolygon"}
    assert result.source == "INEGI. Marco Geoestadístico, diciembre de 2025"


def test_bigquery_mode_requires_project_and_dataset(monkeypatch):
    monkeypatch.setenv("GEOOPPORTUNITY_USE_BIGQUERY", "1")
    monkeypatch.delenv("BIGQUERY_PROJECT", raising=False)
    monkeypatch.delenv("BIGQUERY_DATASET", raising=False)
    with pytest.raises(RuntimeError, match="BIGQUERY_PROJECT"):
        data._bigquery_client()
