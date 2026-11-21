from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sensor import SensorReading
from app.models.irrigation import Irrigation


MOISTURE_THRESHOLD = 30
MIN_WATER_LEVEL = 10


def check_automatic_irrigation(db: Session):
    # Get latest sensor reading
    reading = (
        db.query(SensorReading)
        .order_by(SensorReading.created_at.desc())
        .first()
    )

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="No sensor data available"
        )

    if reading.soil_moisture is None:
        raise HTTPException(
            status_code=400,
            detail="Soil moisture data is missing"
        )

    if reading.water_level is None:
        raise HTTPException(
            status_code=400,
            detail="Water level data is missing"
        )

    # Automatic decision
    if reading.water_level < MIN_WATER_LEVEL:
        pump_status = False
        reason = "Water tank level is too low"

    elif reading.soil_moisture < MOISTURE_THRESHOLD:
        pump_status = True
        reason = "Soil moisture is low"

    else:
        pump_status = False
        reason = "Soil moisture is sufficient"

    # Save decision in database
    irrigation = Irrigation(
        pump_status=pump_status,
        mode="automatic"
    )

    db.add(irrigation)
    db.commit()
    db.refresh(irrigation)

    return {
        "pump_status": pump_status,
        "mode": "automatic",
        "reason": reason,
        "soil_moisture": reading.soil_moisture,
        "water_level": reading.water_level,
        "irrigation_id": irrigation.id
    }