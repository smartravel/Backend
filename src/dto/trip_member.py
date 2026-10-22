from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.core.enums import TripRole

@dataclass
class TripMemberDTO:
    trip_id: UUID
    user_id: UUID
    nickname: str
    avatar_emoji: str | None
    role: TripRole
    joined_at: datetime