from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

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