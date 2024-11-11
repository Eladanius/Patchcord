from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth.auth_service import AuthService
from app.db.models import User, UserStatus
from app.utils.auth_utils import create_access_token, hash_password, verify_password
from app.utils.dependencies import get_current_user
from app.schemas.user_create_request import UserCreateRequest

router = APIRouter()
auth_service = AuthService()

@router.get("/google")
async def auth_google(request: Request):
    return await auth_service.google_authorize(request)

@router.get("/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    token_data = await auth_service.google_callback(request, db)
    if not token_data:
        raise HTTPException(status_code=400, detail="Auth error")
    return token_data


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    offline_status = db.query(UserStatus).filter(UserStatus.status == "offline").first()
    if not offline_status:
        raise HTTPException(status_code=500, detail="Offline status not found in the database")

    hashed_password = hash_password(user_data.password.get_secret_value())
    user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password, status_id=offline_status.id )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.last_status_id = user.status_id
    
    offline_status = db.query(UserStatus).filter(UserStatus.status == "offline").first()
    if not offline_status:
        raise HTTPException(status_code=500, detail="Offline status not found in the database")

    user.status_id = offline_status.id
    db.commit()

    return {"message": "Successfully logged out"}