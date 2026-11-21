
from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class CropCreate(BaseModel):
    crop_name: str = Field(min_length=2, max_length=100)
    season: str = Field(min_length=2, max_length=50)
    soil_type: str | None = None
    planting_date: date | None = None
    notes: str | None = None


class CropResponse(BaseModel):
    id: int
    crop_name: str
    season: str
    soil_type: str | None
    planting_date: date | None
    notes: str | None

    model_config = ConfigDict(from_attributes=True)
