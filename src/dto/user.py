from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class UserDTO:
    user_id: UUID
    email: str
    nickname: str
    avatar_emoji: str | None
    created_at: datetime

@dataclass
class AuthDTO:
    user_id: UUID
    email: str
    nickname: str
    avatar_emoji: str | None
    created_at: datetime
    access_token: str
    refresh_token: str

@dataclass
class StatusDTO:
    status: str