from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"), nullable=False
    )

    soil_moisture: Mapped[float | None] = mapped_column(Float)
    soil_temperature: Mapped[float | None] = mapped_column(Float)
    soil_ph: Mapped[float | None] = mapped_column(Float)

    nitrogen: Mapped[float | None] = mapped_column(Float)
    phosphorus: Mapped[float | None] = mapped_column(Float)
    potassium: Mapped[float | None] = mapped_column(Float)

    water_level: Mapped[float | None] = mapped_column(Float)
    water_flow: Mapped[float | None] = mapped_column(Float)
    proximity_cm: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )