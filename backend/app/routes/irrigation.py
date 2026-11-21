from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.irrigation_service import (
    check_automatic_irrigation
)  

from app.database.connection import get_db
from app.models.irrigation import Irrigation
from app.schemas.irrigation import (
    IrrigationControl,
    IrrigationResponse
)

router = APIRouter(prefix="/irrigation", tags=["Irrigation"])


@router.post("/control", response_model=IrrigationResponse)
def control_pump(
    data: IrrigationControl,
    db: Session = Depends(get_db)
):
    if data.mode not in ["manual", "automatic"]:
        raise HTTPException(
            status_code=400,
            detail="Mode must be manual or automatic"
        )

    irrigation = Irrigation(
        pump_status=data.pump_status,
        mode=data.mode
    )

    db.add(irrigation)
    db.commit()
    db.refresh(irrigation)

    return irrigation


@router.get("/history", response_model=list[IrrigationResponse])
def irrigation_history(db: Session = Depends(get_db)):
    return (
        db.query(Irrigation)
        .order_by(Irrigation.id.desc())
        .limit(50)
        .all()
    )

@router.post("/automatic-check")
def automatic_irrigation_check(
    db: Session = Depends(get_db)
):
    return check_automatic_irrigation(db)