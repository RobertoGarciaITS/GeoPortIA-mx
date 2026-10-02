from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import Business, Municipality, NearbyResponse
from app.services.data import businesses, municipality, nearby

app = FastAPI(title="GeoOpportunity MX API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/municipality", response_model=Municipality)
def get_municipality():
    return municipality()


@app.get("/api/businesses", response_model=list[Business])
def get_businesses():
    return businesses()


@app.get("/api/businesses/{business_id}", response_model=Business)
def get_business(business_id: str):
    result = next((item for item in businesses() if item.business_id == business_id), None)
    if result is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return result


@app.get("/api/nearby", response_model=NearbyResponse)
def get_nearby(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_m: float = Query(..., gt=0, le=100_000),
):
    result = nearby(lat, lng, radius_m)
    return NearbyResponse(latitude=lat, longitude=lng, radius_m=radius_m, count=len(result), businesses=result)
