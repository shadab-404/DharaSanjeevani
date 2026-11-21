from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Irrigation(Base):
    __tablename__ = "irrigations"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    pump_status: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    mode: Mapped[str] = mapped_column(
        String(20), default="automatic"
    )

    water_used: Mapped[float | None] = mapped_column(Float)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    stopped_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )