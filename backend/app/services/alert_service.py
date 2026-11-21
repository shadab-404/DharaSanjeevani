from sqlalchemy.orm import Session

from app.models.sensor import SensorReading
from app.models.alert import Alert


def generate_sensor_alerts(db: Session):

    reading = (
        db.query(SensorReading)
        .order_by(SensorReading.created_at.desc())
        .first()
    )

    if not reading:
        return {"message": "No sensor data available"}

    alerts_created = []

    # Low soil moisture
    if (
        reading.soil_moisture is not None
        and reading.soil_moisture < 30
    ):
        title = "Low Soil Moisture"
        message = "Soil moisture is below 30%. Irrigation may be required."

        existing = db.query(Alert).filter(
            Alert.title == title,
            Alert.is_resolved == False
        ).first()

        if not existing:
            alert = Alert(
                title=title,
                message=message,
                severity="warning"
            )
            db.add(alert)
            alerts_created.append(title)

    # Low water level
    if (
        reading.water_level is not None
        and reading.water_level < 10
    ):
        title = "Low Water Tank Level"
        message = "Water tank level is below 10%."

        existing = db.query(Alert).filter(
            Alert.title == title,
            Alert.is_resolved == False
        ).first()

        if not existing:
            alert = Alert(
                title=title,
                message=message,
                severity="critical"
            )
            db.add(alert)
            alerts_created.append(title)

    db.commit()

    return {
        "message": "Alert check completed",
        "alerts_created": alerts_created
    }