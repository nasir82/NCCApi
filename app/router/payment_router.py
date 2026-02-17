from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(prefix="/payments", tags=["Payments"])

# CREATE
@router.post("/", response_model=schemas.PaymentTrackingResponse, status_code=201)
def create_payment_tracking(data: schemas.PaymentTrackingCreate, db: Session = Depends(get_db)):
    new_record = models.PaymentTracking(**data.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# READ ALL
@router.get("/", response_model=List[schemas.PaymentTrackingResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return db.query(models.PaymentTracking).all()

# UPDATE (Full Update)
@router.put("/{id}", response_model=schemas.PaymentTrackingResponse)
def update_payment_tracking(id: str, update_data: schemas.PaymentTrackingCreate, db: Session = Depends(get_db)):
    query = db.query(models.PaymentTracking).filter(models.PaymentTracking.id == id)
    db_record = query.first()
    
    if not db_record:
        raise HTTPException(status_code=404, detail="Payment record not found")
    
    query.update(update_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(db_record)
    return db_record

# DELETE
@router.delete("/{id}")
def delete_payment_tracking(id: str, db: Session = Depends(get_db)):
    db_record = db.query(models.PaymentTracking).filter(models.PaymentTracking.id == id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    info = {"level": db_record.level, "year": db_record.year}
    db.delete(db_record)
    db.commit()
    return {"message": "Deleted", "info": info}