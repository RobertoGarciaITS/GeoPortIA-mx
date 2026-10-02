from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_ten_baseline_businesses():
    response = client.get("/api/businesses")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 10
    assert len({item["business_id"] for item in payload}) == 10
    assert all(-90 <= item["latitude"] <= 90 for item in payload)
    assert all(-180 <= item["longitude"] <= 180 for item in payload)


def test_municipality_has_geojson_geometry():
    response = client.get("/api/municipality")
    assert response.status_code == 200
    payload = response.json()
    assert payload["cvegeo"] == "05030"
    assert payload["municipality_name"] == "Saltillo"
    assert payload["geometry"]["type"] == "Polygon"
    assert len(payload["geometry"]["coordinates"][0]) >= 4


def test_business_detail_returns_expected_schema():
    response = client.get("/api/businesses/saltillo-001")
    assert response.status_code == 200
    assert response.json()["name"] == "Panadería Alameda"
    assert response.json()["source_record_id"] == "DENUE-FIX-001"


def test_nearby_is_deterministic():
    response = client.get("/api/nearby?lat=25.438&lng=-100.973&radius_m=2000")
    assert response.status_code == 200
    assert response.json()["count"] == 5


def test_missing_business():
    assert client.get("/api/businesses/unknown").status_code == 404


def test_nearby_rejects_invalid_coordinates_and_radius():
    assert client.get("/api/nearby?lat=91&lng=-100&radius_m=2000").status_code == 422
    assert client.get("/api/nearby?lat=25&lng=-181&radius_m=2000").status_code == 422
    assert client.get("/api/nearby?lat=25&lng=-100&radius_m=0").status_code == 422
    assert client.get("/api/nearby?lat=25&lng=-100&radius_m=100001").status_code == 422


def test_nearby_requires_all_parameters():
    assert client.get("/api/nearby?lat=25.438&lng=-100.973").status_code == 422


def test_openapi_exposes_baseline_routes():
    paths = client.get("/openapi.json").json()["paths"]
    assert {"/health", "/api/municipality", "/api/businesses", "/api/businesses/{business_id}", "/api/nearby"} <= set(paths)
