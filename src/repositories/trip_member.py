from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from src.core.enums import TripRole
from src.dto.trip_member import TripMemberDTO
from src.models.trip_member import TripMember
from src.repositories.base import BaseRepository

class TripMemberRepository(BaseRepository):
    async def get_role(self, trip_id: UUID, user_id: UUID) -> TripRole | None:
        result = await self._session.execute(
            select(TripMember.role).where(TripMember.trip_id == trip_id, TripMember.user_id == user_id)
        )
        role = result.scalar_one_or_none()
        if not role:
            return None

        return TripRole(role)

    async def list_by_trip(self, trip_id: UUID) -> list[TripMemberDTO]:
        result = await self._session.execute(
            select(TripMember)
            .options(joinedload(TripMember.user))
            .where(TripMember.trip_id == trip_id)
            .order_by(TripMember.joined_at)
        )

        return [self._to_dto(member) for member in result.scalars().all()]

    async def list_by_trips(self, trip_ids: list[UUID]) -> list[TripMemberDTO]:
        if not trip_ids:
            return []
        result = await self._session.execute(
            select(TripMember)
            .options(joinedload(TripMember.user))
            .where(TripMember.trip_id.in_(trip_ids))
            .order_by(TripMember.joined_at)
        )

        return [self._to_dto(member) for member in result.scalars().all()]

    async def count_by_trip(self, trip_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(TripMember).where(TripMember.trip_id == trip_id)
        )

        return result.scalar_one()

    async def add(self, trip_id: UUID, user_id: UUID, role: TripRole = TripRole.MEMBER) -> None:
        self._session.add(TripMember(trip_id=trip_id, user_id=user_id, role=role))
        await self._session.flush()

    @staticmethod
    def _to_dto(member: TripMember) -> TripMemberDTO:
        return TripMemberDTO(
            trip_id=member.trip_id,
            user_id=member.user_id,
            nickname=member.user.nickname,
            avatar_emoji=member.user.avatar_emoji,
            role=TripRole(member.role),
            joined_at=member.joined_at,
        )