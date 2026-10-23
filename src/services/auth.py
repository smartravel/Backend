from uuid import UUID

from fastapi import Response
from sqlalchemy.exc import IntegrityError

from src.core.cookies import clear_auth_cookies
from src.core.exceptions import EmailTaken, InvalidCredentials, Unauthed
from src.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from src.core.uow import UnitOfWork
from src.dto.user import AuthDTO, StatusDTO, UserDTO

class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register(
        self,
        email: str,
        password: str,
        nickname: str,
        avatar_emoji: str | None,
    ) -> UserDTO:
        if await self.uow.user.get_by_email(email):
            raise EmailTaken

        try:
            return await self.uow.user.create(
                email=email,
                password_hash=await hash_password(password),
                nickname=nickname,
                avatar_emoji=avatar_emoji,
            )
        except IntegrityError:
            raise EmailTaken

    async def login(self, email: str, password: str) -> AuthDTO:
        user = await self.uow.user.get_by_email(email)
        password_hash = await self.uow.user.get_password_hash(email) if user else None

        is_valid = await verify_password(password, password_hash or DUMMY_PASSWORD_HASH)
        if not user or not is_valid:
            raise InvalidCredentials

        return AuthDTO(
            user_id=user.user_id,
            email=user.email,
            nickname=user.nickname,
            avatar_emoji=user.avatar_emoji,
            created_at=user.created_at,
            access_token=create_access_token(user.user_id),
            refresh_token=create_refresh_token(user.user_id),
        )

    async def refresh(self, refresh_token: str | None) -> str:
        if not refresh_token:
            raise Unauthed

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise Unauthed

        user_id = UUID(payload["sub"])
        if not await self.uow.user.get_by_id(user_id):
            raise Unauthed

        return create_access_token(user_id)

    async def logout(self, response: Response) -> StatusDTO:
        clear_auth_cookies(response)
        return StatusDTO(status="logged_out")

    async def get_profile(self, access_token: str | None) -> UserDTO:
        user_id = self._get_user_id(access_token)

        user = await self.uow.user.get_by_id(user_id)
        if not user:
            raise Unauthed

        return user

    def _get_user_id(self, access_token: str | None) -> UUID:
        if not access_token:
            raise Unauthed

        payload = decode_token(access_token)
        if not payload or payload.get("type") != "access":
            raise Unauthed

        return UUID(payload["sub"])