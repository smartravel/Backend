import datetime as dt
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from src.core.enums import TripRole

if TYPE_CHECKING:
    from src.models.trip import Trip
    from src.models.user import User

class TripMember(Base):
    __tablename__ = "trip_members"
    __table_args__ = (
        CheckConstraint("role IN ('organizer', 'member')", name="ck_trip_members_role"),
    )

    trip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(20), default=TripRole.MEMBER)
    joined_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    trip: Mapped["Trip"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship()