from fastapi import APIRouter, Depends, Request

from app.db.models import User
from app.utils.dependencies import get_current_user


router = APIRouter()

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}