from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.post("/", response_model=schemas.ExamResponse, status_code=201)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    db_exam = models.Exam(**exam.model_dump())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

@router.get("/", response_model=List[schemas.ExamResponse])
def get_all_exams(db: Session = Depends(get_db)):
    return db.query(models.Exam).all()

@router.get("/{ref}", response_model=schemas.ExamResponse)
def get_exam(ref: str, db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.ref == ref).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.patch("/{ref}", response_model=schemas.ExamResponse)
def update_exam(ref: str, exam_update: schemas.ExamCreate, db: Session = Depends(get_db)):
    query = db.query(models.Exam).filter(models.Exam.ref == ref)
    db_exam = query.first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    query.update(exam_update.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_exam)
    return db_exam

@router.delete("/{ref}")
def delete_exam(ref: str, db: Session = Depends(get_db)):
    query = db.query(models.Exam).filter(models.Exam.ref == ref)
    db_exam = query.first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    data = {"title": db_exam.examTitle, "subject": db_exam.subject}
    query.delete()
    db.commit()
    return {"message": "Deleted successfully", "data": data}