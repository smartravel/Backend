from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

@dataclass
class NotificationDTO:
    id: UUID
    trip_id: UUID | None
    type: str
    payload: dict[str, Any]
    created_at: datetime
    read_at: datetime | None