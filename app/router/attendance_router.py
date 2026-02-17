from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix='/attendance-tracking',
    tags=['Attendance Tracking']
)

# CREATE
@router.post("/", response_model=schemas.AttendanceTrackingResponse, status_code=201)
def create_tracking(data: schemas.AttendanceTrackingCreate, db: Session = Depends(get_db)):
    new_track = models.AttendanceTracking(**data.model_dump())
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return new_track

# READ ALL
@router.get("/", response_model=List[schemas.AttendanceTrackingResponse])
def get_all_tracking(db: Session = Depends(get_db)):
    return db.query(models.AttendanceTracking).all()

# READ ONE
@router.get("/{id}", response_model=schemas.AttendanceTrackingResponse)
def get_one_tracking(id: str, db: Session = Depends(get_db)):
    track = db.query(models.AttendanceTracking).filter(models.AttendanceTracking.id == id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return track

# UPDATE (Adding a new attendance record to the list)
@router.patch("/{id}", response_model=schemas.AttendanceTrackingResponse)
def add_attendance_record(id: str, record: schemas.AttendanceModelSchema, db: Session = Depends(get_db)):
    track = db.query(models.AttendanceTracking).filter(models.AttendanceTracking.id == id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Tracking record not found")

    # Update the JSON list
    current_records = list(track.attendance_records)
    current_records.append(record.model_dump())
    
    # Re-assign to trigger SQLAlchemy update
    track.attendance_records = current_records
    
    db.commit()
    db.refresh(track)
    return track

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tracking(id: str, db: Session = Depends(get_db)):
    track = db.query(models.AttendanceTracking).filter(models.AttendanceTracking.id == id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    
    db.delete(track)
    db.commit()
    return None