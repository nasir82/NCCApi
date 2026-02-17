from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.post("/", response_model=schemas.ResourceResponse, status_code=201)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    db_resource = models.Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.get("/", response_model=List[schemas.ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).all()

@router.get("/{id}", response_model=schemas.ResourceResponse)
def get_resource(id: str, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(models.Resource.id == id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.patch("/{id}", response_model=schemas.ResourceResponse)
def update_resource(id: str, resource_update: schemas.ResourceCreate, db: Session = Depends(get_db)):
    query = db.query(models.Resource).filter(models.Resource.id == id)
    if not query.first():
        raise HTTPException(status_code=404, detail="Resource not found")
    
    query.update(resource_update.model_dump(exclude_unset=True))
    db.commit()
    return query.first()

@router.delete("/{id}")
def delete_resource(id: str, db: Session = Depends(get_db)):
    db_resource = db.query(models.Resource).filter(models.Resource.id == id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    deleted_data = {"title": db_resource.title, "type": db_resource.type}
    db.delete(db_resource)
    db.commit()
    return {"message": "Resource deleted successfully", "data": deleted_data}