from uuid import UUID

from sqlalchemy import select

from src.dto.user import UserDTO
from src.models.user import User
from src.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    async def get_by_id(self, user_id: UUID) -> UserDTO | None:
        result = await self._session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None

        return self._to_dto(user)

    async def get_by_email(self, email: str) -> UserDTO | None:
        result = await self._session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            return None

        return self._to_dto(user)

    async def get_password_hash(self, email: str) -> str | None:
        result = await self._session.execute(select(User.password_hash).where(User.email == email))

        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        password_hash: str,
        nickname: str,
        avatar_emoji: str | None = None,
    ) -> UserDTO:
        user = User(
            email=email,
            password_hash=password_hash,
            nickname=nickname,
            avatar_emoji=avatar_emoji,
        )
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)

        return self._to_dto(user)

    @staticmethod
    def _to_dto(user: User) -> UserDTO:
        return UserDTO(
            user_id=user.user_id,
            email=user.email,
            nickname=user.nickname,
            avatar_emoji=user.avatar_emoji,
            created_at=user.created_at,
        )