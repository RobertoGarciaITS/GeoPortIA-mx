from typing import Any
from pydantic import BaseModel, Field


class Business(BaseModel):
    business_id: str
    source_record_id: str
    name: str
    scian: str
    economic_activity: str
    employee_range: str
    latitude: float
    longitude: float
    municipality_id: str
    source: str
    geography: dict[str, Any] | None = None


class Municipality(BaseModel):
    municipality_id: str
    cvegeo: str
    municipality_name: str
    state_name: str
    source: str
    geometry: dict[str, Any]


class NearbyResponse(BaseModel):
    latitude: float
    longitude: float
    radius_m: float = Field(gt=0)
    count: int
    businesses: list[Business]
