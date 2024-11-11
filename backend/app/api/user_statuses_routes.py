from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from app.db.database import get_db
from app.db.models.user_status import UserStatus


router = APIRouter()

@router.get('/')
async def get_statuses(db: Session = Depends(get_db)):
    return db.query(UserStatus).all()

@router.get('/{id}')
async def get_statuses(id:int, db: Session = Depends(get_db)):
    status = db.query(UserStatus).filter(UserStatus.id==id).first()
    if status:
        return status
    else:
        raise HTTPException(status_code=404, detail="User status not found")
