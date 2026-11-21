
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.crop import Crop
from app.schemas.crop import CropCreate, CropResponse

router = APIRouter(prefix="/crops", tags=["Crops"])


# Add a new crop
@router.post("/", response_model=CropResponse, status_code=201)
def create_crop(
    data: CropCreate,
    db: Session = Depends(get_db)
):
    crop = Crop(
        crop_name=data.crop_name,
        season=data.season,
        soil_type=data.soil_type,
        planting_date=data.planting_date,
        notes=data.notes
    )

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return crop


# Get all crops
@router.get("/", response_model=list[CropResponse])
def get_crops(db: Session = Depends(get_db)):
    return db.query(Crop).order_by(Crop.id.desc()).all()


# Get one crop
@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(
    crop_id: int,
    db: Session = Depends(get_db)
):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if not crop:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    return crop


# Delete a crop
@router.delete("/{crop_id}")
def delete_crop(
    crop_id: int,
    db: Session = Depends(get_db)
):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if not crop:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    db.delete(crop)
    db.commit()

    return {"message": "Crop deleted successfully"}
