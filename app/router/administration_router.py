from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.models import models
from sqlalchemy.orm import Session

from app.schemas import schemas

router = APIRouter(
    prefix='/administration',
    tags=['Administration']
)

@router.post("/", status_code=201, response_model=schemas.OfficialPersonResponse)
def create_official(person: schemas.OfficialPersonCreate, db: Session = Depends(get_db)):
    db_person = models.OfficialPerson(**person.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.get("/", response_model=List[schemas.OfficialPersonResponse])
def get_officials(db: Session = Depends(get_db)):
    return db.query(models.OfficialPerson).all()

@router.patch("/{ref}", response_model=schemas.OfficialPersonResponse)
def update_official(
    ref: str, 
    person_update: schemas.OfficialPersonCreate, 
    db: Session = Depends(get_db)
):
    query = db.query(models.OfficialPerson).filter(models.OfficialPerson.ref == ref)
    db_person = query.first()

    if not db_person:
        raise HTTPException(
            status_code=404, 
            detail=f"Official person with ref {ref} not found"
        )

    update_data = person_update.model_dump(exclude_unset=True)

    query.update(update_data, synchronize_session=False)
    
    db.commit()
    
    db.refresh(db_person)
    
    return db_person


@router.delete("/{ref}", response_model=schemas.OfficialPersonResponse)
def delete_official(ref: str, db: Session = Depends(get_db)):
    # 1. Find the person
    query = db.query(models.OfficialPerson).filter(models.OfficialPerson.ref == ref)
    db_person = query.first()

    if not db_person:
        raise HTTPException(status_code=404, detail="Official person not found")

    # 2. Store the data in a variable before deleting
    deleted_person_data = db_person

    # 3. Delete from database
    query.delete(synchronize_session=False)
    db.commit()
    
    # 4. Return the data (FastAPI will show name, designation, etc.)
    return deleted_person_data