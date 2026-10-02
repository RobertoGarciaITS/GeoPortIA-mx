from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_ten_baseline_businesses():
    response = client.get("/api/businesses")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_nearby_is_deterministic():
    response = client.get("/api/nearby?lat=25.438&lng=-100.973&radius_m=2000")
    assert response.status_code == 200
    assert response.json()["count"] == 5


def test_missing_business():
    assert client.get("/api/businesses/unknown").status_code == 404
