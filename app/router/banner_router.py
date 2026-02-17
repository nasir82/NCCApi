from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.models import models
from sqlalchemy.orm import Session

from app.schemas import schemas

router = APIRouter(
    prefix='/banner',
    tags=['Banners']
)


@router.post("/", status_code=201,response_model=schemas.BannerResponse)
def create_banner(banner: schemas.BannerCreate, db:Session = Depends(get_db)):
    new_banner = models.Banner(**banner.model_dump())
    db.add(new_banner)
    db.commit()
    db.refresh(new_banner)
    return new_banner


@router.get("/")
def get_banner(db:Session = Depends(get_db)):
    """
    Getting all banners from the database. If there are no banners, it returns an empty list.
    """
    db_banners = db.query(models.Banner).all()
    if db_banners:
        print(len(db_banners))
        return db_banners
    return []




@router.get("/{ref}")
def get_banner_by_ref(ref: str, db:Session = Depends(get_db)):
    banner = db.query(models.Banner).filter(models.Banner.ref == ref).first()
    if not banner:
        raise HTTPException(status_code=404, detail=f"Banner with ref {ref} not found")
    return banner


@router.patch("/{ref}")
def update_banner(ref: str, banner_update: schemas.BannerCreate, db:Session = Depends(get_db)):
    banner = db.query(models.Banner).filter(models.Banner.ref == ref).first()
    if not banner:
        raise HTTPException(status_code=404, detail=f"Banner with ref {ref} not found")
    
    for key, value in banner_update.model_dump().items():
        setattr(banner, key, value)
    
    db.commit()
    db.refresh(banner)
    return banner

@router.delete("/{ref}", status_code=204)
def delete_banner(ref: str, db:Session = Depends(get_db)):
    banner = db.query(models.Banner).filter(models.Banner.ref == ref).first()
    if not banner:
        raise HTTPException(status_code=404, detail=f"Banner with ref {ref} not found")
    db.delete(banner)
    db.commit()
    return {"detail": f"Banner with ref {ref} deleted successfully"}