from datetime import date, datetime
from datetime import time as Time
from uuid import UUID
from pydantic import BaseModel, Field

class TripPointCreateRequest(BaseModel):
    id: UUID | None = None
    day_date: date
    title: str = Field(..., min_length=1, max_length=200)
    time: Time | None = None
    note: str | None = Field(None, max_length=2000)
    position: float | None = None

class TripPointUpdateRequest(BaseModel):
    day_date: date | None = None
    title: str | None = Field(None, min_length=1, max_length=200)
    time: Time | None = None
    note: str | None = Field(None, max_length=2000)
    position: float | None = None

class TripPointResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    day_date: date
    position: float
    title: str
    time: Time | None
    note: str | None
    created_by: UUID
    updated_at: datetime

class RouteDayResponse(BaseModel):
    date: date
    day_number: int
    points: list[TripPointResponse]

class RouteResponse(BaseModel):
    days: list[RouteDayResponse]