from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel

class NotificationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    trip_id: UUID | None
    type: str
    payload: dict[str, Any]
    created_at: datetime
    read_at: datetime | None

class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    unread_count: int