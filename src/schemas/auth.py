from pydantic import BaseModel, EmailStr, Field, field_validator
from src.schemas.user import check_avatar_emoji

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    nickname: str = Field(..., min_length=1, max_length=50)
    avatar_emoji: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Ник не может быть пустым")
        return value

    @field_validator("avatar_emoji")
    @classmethod
    def validate_avatar(cls, value: str | None) -> str | None:
        return check_avatar_emoji(value)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

class StatusResponse(BaseModel):
    status: str