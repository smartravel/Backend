from dataclasses import dataclass
from datetime import date, datetime
from datetime import time as Time
from decimal import Decimal
from uuid import UUID

@dataclass
class TripPointDTO:
    id: UUID
    trip_id: UUID
    day_date: date
    position: Decimal
    title: str
    time: Time | None
    note: str | None
    created_by: UUID
    created_at: datetime
    updated_at: datetime