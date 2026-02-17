from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=schemas.TeacherResponse, status_code=201)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    """
    **Register a new teacher.**
    
    This endpoint creates a teacher profile. Note that the **email must be unique** across the entire system.
    """
    db_teacher = models.Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/", response_model=List[schemas.TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()

@router.get("/{id}", response_model=schemas.TeacherResponse)
def get_teacher(id: str, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.patch("/{id}", response_model=schemas.TeacherResponse)
def update_teacher(id: str, update: schemas.TeacherCreate, db: Session = Depends(get_db)):
    query = db.query(models.Teacher).filter(models.Teacher.id == id)
    db_teacher = query.first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    query.update(update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.delete("/{id}")
def delete_teacher(id: str, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db.delete(db_teacher)
    db.commit()
    return {"message": f"Teacher {db_teacher.name} removed successfully"}