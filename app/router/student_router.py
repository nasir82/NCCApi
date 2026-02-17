from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/students',
    tags=['Students']
)


@router.post("/students", status_code=201, response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/students", response_model=List[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    # Fetch all student records from the students table
    students = db.query(models.Student).all()
    return students

@router.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404, 
            detail=f"Student with id {student_id} not found"
        )
    return student


#delete student by id   
@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404, 
            detail=f"Student with id {student_id} not found"
        )
    
    db.delete(student)
    db.commit()
    return