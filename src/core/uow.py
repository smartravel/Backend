from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import AsyncSessionLocal
from src.repositories.notification import NotificationRepository
from src.repositories.trip import TripRepository
from src.repositories.trip_member import TripMemberRepository
from src.repositories.trip_point import TripPointRepository
from src.repositories.user import UserRepository

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = UserRepository(self.session)
        self.trip = TripRepository(self.session)
        self.trip_member = TripMemberRepository(self.session)
        self.trip_point = TripPointRepository(self.session)
        self.notification = NotificationRepository(self.session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()

@asynccontextmanager
async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with AsyncSessionLocal() as session:
        uow = UnitOfWork(session)
        try:
            yield uow
            await uow.commit()
        except Exception:
            await uow.rollback()
            raise