
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.device import Device
from app.models.sensor import SensorReading
from app.schemas.sensor import SensorDataCreate, SensorDataResponse

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/data", response_model=SensorDataResponse)
def receive_sensor_data(
    data: SensorDataCreate,
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(
        Device.device_code == data.device_code
    ).first()

    if not device:
        device = Device(
            device_code=data.device_code,
            device_name=data.device_code,
            is_online=True
        )
        db.add(device)
        db.flush()

    device.is_online = True

    reading = SensorReading(
        device_id=device.id,
        soil_moisture=data.soil_moisture,
        soil_temperature=data.soil_temperature,
        soil_ph=data.soil_ph,
        nitrogen=data.nitrogen,
        phosphorus=data.phosphorus,
        potassium=data.potassium,
        water_level=data.water_level,
        water_flow=data.water_flow,
        proximity_cm=data.proximity_cm
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return reading


@router.get("/latest", response_model=SensorDataResponse)
def get_latest_reading(db: Session = Depends(get_db)):
    reading = (
        db.query(SensorReading)
        .order_by(SensorReading.created_at.desc())
        .first()
    )

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="No sensor readings found"
        )

    return reading


@router.get("/history", response_model=list[SensorDataResponse])
def get_sensor_history(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 500"
        )

    readings = (
        db.query(SensorReading)
        .order_by(SensorReading.created_at.desc())
        .limit(limit)
        .all()
    )

    return readings
