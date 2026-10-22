from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from src.dto.trip_point import TripPointDTO
from src.models.trip_point import TripPoint
from src.repositories.base import BaseRepository

class TripPointRepository(BaseRepository):
    async def get(self, trip_id: UUID, point_id: UUID) -> TripPointDTO | None:
        point = await self._get_model(trip_id, point_id)
        if not point:
            return None

        return self._to_dto(point)

    async def list_by_trip(self, trip_id: UUID) -> list[TripPointDTO]:
        result = await self._session.execute(
            select(TripPoint)
            .where(TripPoint.trip_id == trip_id)
            .order_by(TripPoint.day_date, TripPoint.position)
        )

        return [self._to_dto(point) for point in result.scalars().all()]

    async def max_position(self, trip_id: UUID, day_date: date) -> Decimal | None:
        result = await self._session.execute(
            select(func.max(TripPoint.position)).where(
                TripPoint.trip_id == trip_id, TripPoint.day_date == day_date
            )
        )

        return result.scalar_one()

    async def create(self, trip_id: UUID, created_by: UUID, data: dict) -> TripPointDTO:
        if data.get("id") is None:
            data.pop("id", None)
        point = TripPoint(trip_id=trip_id, created_by=created_by, **data)
        self._session.add(point)
        await self._session.flush()
        await self._session.refresh(point)

        return self._to_dto(point)

    async def update(self, trip_id: UUID, point_id: UUID, data: dict) -> TripPointDTO | None:
        point = await self._get_model(trip_id, point_id)
        if not point:
            return None
        for field, value in data.items():
            setattr(point, field, value)
        await self._session.flush()
        await self._session.refresh(point)

        return self._to_dto(point)

    async def delete(self, trip_id: UUID, point_id: UUID) -> bool:
        point = await self._get_model(trip_id, point_id)
        if not point:
            return False
        await self._session.delete(point)
        await self._session.flush()

        return True

    async def _get_model(self, trip_id: UUID, point_id: UUID) -> TripPoint | None:
        result = await self._session.execute(
            select(TripPoint).where(TripPoint.trip_id == trip_id, TripPoint.id == point_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    def _to_dto(point: TripPoint) -> TripPointDTO:
        return TripPointDTO(
            id=point.id,
            trip_id=point.trip_id,
            day_date=point.day_date,
            position=point.position,
            title=point.title,
            time=point.time,
            note=point.note,
            created_by=point.created_by,
            created_at=point.created_at,
            updated_at=point.updated_at,
        )