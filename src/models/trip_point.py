import datetime as dt
import uuid
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base

class TripPoint(Base):
    __tablename__ = "trip_points"
    __table_args__ = (
        Index("ix_trip_points_trip_day_position", "trip_id", "day_date", "position"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"))
    day_date: Mapped[dt.date]
    position: Mapped[Decimal] = mapped_column(Numeric)
    title: Mapped[str] = mapped_column(String(200))
    time: Mapped[dt.time | None]
    note: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )