from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..schemas import schemas
from ..models import models

router = APIRouter(
    prefix="/events",
    tags=["Events"] # Groups them together in the /docs UI
)

@router.post("/", response_model=schemas.EventResponse, status_code=201)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@router.get("/{id}", response_model=schemas.EventResponse)
def get_event(id: str, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.delete("/{id}")
def delete_event(id: str, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": f"Event '{db_event.title}' deleted"}