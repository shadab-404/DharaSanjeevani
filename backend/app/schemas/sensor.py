
from datetime import datetime

from pydantic import BaseModel, Field


class SensorDataCreate(BaseModel):
    device_code: str = Field(min_length=1, max_length=100)

    soil_moisture: float | None = Field(default=None, ge=0, le=100)
    soil_temperature: float | None = None
    soil_ph: float | None = Field(default=None, ge=0, le=14)

    nitrogen: float | None = Field(default=None, ge=0)
    phosphorus: float | None = Field(default=None, ge=0)
    potassium: float | None = Field(default=None, ge=0)

    water_level: float | None = Field(default=None, ge=0)
    water_flow: float | None = Field(default=None, ge=0)
    proximity_cm: float | None = Field(default=None, ge=0)


class SensorDataResponse(BaseModel):
    id: int
    device_id: int
    soil_moisture: float | None
    soil_temperature: float | None
    soil_ph: float | None
    nitrogen: float | None
    phosphorus: float | None
    potassium: float | None
    water_level: float | None
    water_flow: float | None
    proximity_cm: float | None
    created_at: datetime

    model_config = {"from_attributes": True}
