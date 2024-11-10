from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth.auth_service import AuthService
from app.db.models import User
from app.utils.auth_utils import create_access_token, hash_password, verify_password
from app.utils.dependencies import get_current_user

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
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")

    hashed_password = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    token = request.headers.get("Authorization").split(" ")[1]  # Извлекаем токен из заголовка
    
    # Обновляем статус пользователя
    user.status = "offline"
    db.commit()
    
    # (Дополнительно) Добавьте токен в чёрный список, если используете его
    # blacklisted_token = BlacklistedToken(token=token)
    # db.add(blacklisted_token)
    # db.commit()

    return {"message": "Successfully logged out"}
