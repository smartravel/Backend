from datetime import date
from uuid import UUID
from sqlalchemy import select
from src.core.enums import TripRole
from src.dto.trip import TripDTO
from src.models.trip import Trip
from src.models.trip_member import TripMember
from src.repositories.base import BaseRepository

class TripRepository(BaseRepository):
    async def get_by_id(self, trip_id: UUID) -> TripDTO | None:
        result = await self._session.execute(select(Trip).where(Trip.id == trip_id))
        trip = result.scalar_one_or_none()
        if not trip:
            return None

        return self._to_dto(trip)

    async def get_by_invite_token(self, invite_token: str) -> TripDTO | None:
        result = await self._session.execute(select(Trip).where(Trip.invite_token == invite_token))
        trip = result.scalar_one_or_none()
        if not trip:
            return None

        return self._to_dto(trip)

    async def get_password_hash(self, trip_id: UUID) -> str | None:
        result = await self._session.execute(select(Trip.password_hash).where(Trip.id == trip_id))

        return result.scalar_one_or_none()

    async def list_for_user(self, user_id: UUID) -> list[tuple[TripDTO, TripRole]]:
        result = await self._session.execute(
            select(Trip, TripMember.role)
            .join(TripMember, TripMember.trip_id == Trip.id)
            .where(TripMember.user_id == user_id)
            .order_by(Trip.start_date)
        )

        return [(self._to_dto(trip), TripRole(role)) for trip, role in result.all()]

    async def create(
        self,
        title: str,
        destination: str | None,
        start_date: date,
        end_date: date,
        password_hash: str,
        invite_token: str,
        created_by: UUID,
    ) -> TripDTO:
        trip = Trip(
            title=title,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            password_hash=password_hash,
            invite_token=invite_token,
            created_by=created_by,
        )
        self._session.add(trip)
        await self._session.flush()
        await self._session.refresh(trip)

        return self._to_dto(trip)

    @staticmethod
    def _to_dto(trip: Trip) -> TripDTO:
        return TripDTO(
            id=trip.id,
            title=trip.title,
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
            invite_token=trip.invite_token,
            created_by=trip.created_by,
            created_at=trip.created_at,
        )