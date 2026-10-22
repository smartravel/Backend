from uuid import UUID
from sqlalchemy import func, select, update
from src.dto.notification import NotificationDTO
from src.models.notification import Notification
from src.repositories.base import BaseRepository

class NotificationRepository(BaseRepository):
    async def list_for_user(self, user_id: UUID, limit: int = 50) -> list[NotificationDTO]:
        result = await self._session.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )

        return [self._to_dto(notification) for notification in result.scalars().all()]

    async def count_unread(self, user_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.read_at.is_(None))
        )

        return result.scalar_one()

    async def mark_read(self, user_id: UUID, notification_id: UUID) -> bool:
        result = await self._session.execute(
            update(Notification)
            .where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
                Notification.read_at.is_(None),
            )
            .values(read_at=func.now())
        )

        return result.rowcount > 0

    async def mark_all_read(self, user_id: UUID) -> None:
        await self._session.execute(
            update(Notification)
            .where(Notification.user_id == user_id, Notification.read_at.is_(None))
            .values(read_at=func.now())
        )

    @staticmethod
    def _to_dto(notification: Notification) -> NotificationDTO:
        return NotificationDTO(
            id=notification.id,
            trip_id=notification.trip_id,
            type=notification.type,
            payload=notification.payload,
            created_at=notification.created_at,
            read_at=notification.read_at,
        )