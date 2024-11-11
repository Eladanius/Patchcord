from fastapi import APIRouter, Depends, status, HTTPException
from requests import Session

from app.db.models import User
from app.utils.dependencies import get_current_user
from app.schemas.status_update_request import StatusUpdateRequest
from app.db.database import get_db
from app.db.models.user_status import UserStatus


router = APIRouter()

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}


@router.patch("/status")
async def update_status(request: StatusUpdateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Получаем новый статус из базы данных
    new_status = db.query(UserStatus).filter(UserStatus.id == request.status_id).first()
    
    # Проверяем, существует ли статус и не является ли он "offline"
    if not new_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    if new_status.status == "offline":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot set status to 'offline'")

    # Обновляем статус пользователя
    user.status_id = new_status.id
    db.commit()
    
    return {"message": "Status updated successfully", "new_status": new_status.status}