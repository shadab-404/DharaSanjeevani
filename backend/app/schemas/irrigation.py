from datetime import datetime
from pydantic import BaseModel, ConfigDict


class IrrigationControl(BaseModel):
    pump_status: bool
    mode: str = "manual"


class IrrigationResponse(BaseModel):
    id: int
    pump_status: bool
    mode: str
    water_used: float | None
    started_at: datetime
    stopped_at: datetime | None

    model_config = ConfigDict(from_attributes=True)