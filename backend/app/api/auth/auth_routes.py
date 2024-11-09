from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.get("/auth/google")
async def auth_google(request: Request):
    return await auth_service.google_authorize(request)

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    token_data = await auth_service.google_callback(request, db)
    if not token_data:
        raise HTTPException(status_code=400, detail="Auth error")
    return token_data
