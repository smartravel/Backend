import datetime as dt
import uuid
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base

class PollVote(Base):
    __tablename__ = "poll_votes"

    poll_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("polls.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    option_id: Mapped[uuid.UUID]
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )