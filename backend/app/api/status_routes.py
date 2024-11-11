from fastapi import APIRouter, Depends
from requests import Session

from app.db.database import get_db
from app.db.models.user_status import UserStatus


router = APIRouter()

@router.get('/')
async def get_statuses(db: Session = Depends(get_db)):
    return db.query(UserStatus).all()