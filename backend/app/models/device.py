from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    device_code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    device_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    is_online: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )