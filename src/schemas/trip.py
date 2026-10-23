from datetime import date
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from src.core.enums import TripRole
from src.schemas.user import UserShortResponse

TripStatus = Literal["upcoming", "ongoing", "finished"]

class TripCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    destination: str | None = Field(None, max_length=120)
    start_date: date
    end_date: date
    password: str = Field(..., min_length=4, max_length=64)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be after start date")
        return self

class TripJoinRequest(BaseModel):
    invite_token: str = Field(..., min_length=1, max_length=32)
    password: str = Field(..., max_length=64)

class TripMemberResponse(BaseModel):
    user_id: UUID
    nickname: str
    avatar_emoji: str | None
    role: TripRole

class TripCardResponse(BaseModel):
    id: UUID
    title: str
    start_date: date
    end_date: date
    status: TripStatus
    days_left: int | None
    my_role: TripRole
    members_count: int
    members: list[UserShortResponse]

class TripCountsResponse(BaseModel):
    all: int
    upcoming: int
    past: int

class TripListResponse(BaseModel):
    items: list[TripCardResponse]
    counts: TripCountsResponse

class TripResponse(BaseModel):
    id: UUID
    title: str
    destination: str | None
    start_date: date
    end_date: date
    status: TripStatus
    days_left: int | None
    my_role: TripRole
    invite_token: str
    members_count: int
    members: list[TripMemberResponse]