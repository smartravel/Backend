from datetime import datetime
from uuid import UUID
import emoji
from pydantic import BaseModel, Field, field_validator

BLOCKED_AVATARS = frozenset("🖕 💩 🍆 🍑 💦 🔞 👅 🤬".split())
_MODIFIERS = dict.fromkeys(map(ord, "\U0001F3FB\U0001F3FC\U0001F3FD\U0001F3FE\U0001F3FF️"))

def check_avatar_emoji(value: str | None) -> str | None:
    if value is None:
        return value
    if not emoji.is_emoji(value):
        raise ValueError("Avatar can be emoji once")
    if value.translate(_MODIFIERS) in BLOCKED_AVATARS:
        raise ValueError("Your avatar is blocked")
    return value

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    user_id: UUID
    email: str
    nickname: str
    avatar_emoji: str | None
    created_at: datetime

class UserShortResponse(BaseModel):
    model_config = {"from_attributes": True}

    user_id: UUID
    nickname: str
    avatar_emoji: str | None

class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(None, min_length=1, max_length=50)
    avatar_emoji: str | None = None

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str | None) -> str:
        if value is None or not value.strip():
            raise ValueError("Nickname cannot be empty")
        return value.strip()

    @field_validator("avatar_emoji")
    @classmethod
    def validate_avatar(cls, value: str | None) -> str | None:
        return check_avatar_emoji(value)