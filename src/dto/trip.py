from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID
from src.core.enums import TripRole
from src.dto.trip_member import TripMemberDTO

@dataclass
class TripDTO:
    id: UUID
    title: str
    destination: str | None
    start_date: date
    end_date: date
    invite_token: str
    created_by: UUID
    created_at: datetime

@dataclass
class TripCardDTO:
    id: UUID
    title: str
    start_date: date
    end_date: date
    status: str
    days_left: int | None
    my_role: TripRole
    members_count: int
    members: list[TripMemberDTO]

@dataclass
class TripCountsDTO:
    all: int
    upcoming: int
    past: int

@dataclass
class TripListDTO:
    items: list[TripCardDTO]
    counts: TripCountsDTO

@dataclass
class TripDetailDTO:
    id: UUID
    title: str
    destination: str | None
    start_date: date
    end_date: date
    status: str
    days_left: int | None
    my_role: TripRole
    invite_token: str
    members_count: int
    members: list[TripMemberDTO]