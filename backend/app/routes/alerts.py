from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.alert import Alert
from app.services.alert_service import generate_sensor_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/check")
def check_alerts(db: Session = Depends(get_db)):
    return generate_sensor_alerts(db)


@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .order_by(Alert.id.desc())
        .limit(50)
        .all()
    )


@router.patch("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.is_resolved = True
    db.commit()

    return {
        "message": "Alert resolved successfully",
        "alert_id": alert.id
    }