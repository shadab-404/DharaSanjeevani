from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    crop_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    season: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    soil_type: Mapped[str | None] = mapped_column(String(100))
    planting_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)