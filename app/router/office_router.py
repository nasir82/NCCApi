from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(prefix="/office", tags=["Office Staff"])

@router.post("/", response_model=schemas.OfficePersonResponse, status_code=201)
def create_staff(person: schemas.OfficePersonCreate, db: Session = Depends(get_db)):
    # Use model_dump(by_alias=True) if names differ significantly
    db_person = models.OfficePerson(
        name=person.name,
        designation=person.designation,
        phone=person.phone,
        email=person.email,
        image=person.image,
        from_date=person.from_date,
        to_date=person.to_date
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.get("/", response_model=List[schemas.OfficePersonResponse])
def get_all_staff(db: Session = Depends(get_db)):
    return db.query(models.OfficePerson).all()
# GET a single staff member by ref
@router.get("/{ref}", response_model=schemas.OfficePersonResponse)
def get_staff_by_ref(ref: str, db: Session = Depends(get_db)):
    db_person = db.query(models.OfficePerson).filter(models.OfficePerson.ref == ref).first()
    
    if not db_person:
        raise HTTPException(
            status_code=404, 
            detail=f"Staff member with ref {ref} not found"
        )
    return db_person

# UPDATE a staff member
@router.patch("/{ref}", response_model=schemas.OfficePersonResponse)
def update_staff(
    ref: str, 
    person_update: schemas.OfficePersonCreate, 
    db: Session = Depends(get_db)
):
    # 1. Locate the existing record
    query = db.query(models.OfficePerson).filter(models.OfficePerson.ref == ref)
    db_person = query.first()

    if not db_person:
        raise HTTPException(status_code=404, detail="Staff member not found")

    # 2. Convert schema to dict, excluding fields that weren't provided in the request
    # This ensures we don't accidentally overwrite existing data with nulls
    update_data = person_update.model_dump(exclude_unset=True)

    # 3. Apply the update
    query.update(update_data, synchronize_session=False)
    
    db.commit()
    db.refresh(db_person)
    return db_person
@router.delete("/{ref}")
def delete_staff(ref: str, db: Session = Depends(get_db)):
    db_person = db.query(models.OfficePerson).filter(models.models.OfficePerson.ref == ref).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    name = db_person.name
    db.delete(db_person)
    db.commit()
    return {"message": f"Successfully removed {name}"}