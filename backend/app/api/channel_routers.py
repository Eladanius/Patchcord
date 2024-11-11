from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.channel import Channel
from app.schemas.channel_create_request import ChannelCreate
from app.db.models.user import User
from app.utils.dependencies import get_current_user
from app.utils.channel_utils import is_channel_admin
from app.schemas.channel_update_request import ChannelUpdate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_channel(channel_data: ChannelCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Проверка уникальности имени канала
    existing_channel = db.query(Channel).filter(Channel.name == channel_data.name).first()
    if existing_channel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Channel with this name already exists"
        )

    # Поиск admin_id по admin_email или использование current_user.id по умолчанию
    admin_id = current_user.id
    if channel_data.admin_email:
        admin = db.query(User).filter(User.email == channel_data.admin_email).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin with this email not found")
        admin_id = admin.id

    # Поиск moderator_id по moderator_email, если указан
    moderator_id = None
    if channel_data.moderator_email:
        moderator = db.query(User).filter(User.email == channel_data.moderator_email).first()
        if not moderator:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Moderator with this email not found")
        moderator_id = moderator.id

    # Создание нового канала
    new_channel = Channel(
        name=channel_data.name,
        is_private=channel_data.is_private,
        topic=channel_data.topic,
        created_by=current_user.id,
        admin_id=admin_id,
        moderator_id=moderator_id
    )
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)

    return {"message": "Channel created successfully", "channel": new_channel}

@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(channel_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Найти канал
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    
    # Проверка прав администратора
    is_channel_admin(current_user.id, channel)

    # Удалить канал
    db.delete(channel)
    db.commit()
    return {"message": "Channel deleted successfully"}

@router.patch("/{channel_id}")
async def update_channel(
    channel_id: UUID,
    channel_data: ChannelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    
    # Проверка прав администратора
    is_channel_admin(current_user.id, channel)

    # Обновляем данные канала, если переданы
    if channel_data.name:
        channel.name = channel_data.name
    
    if channel_data.topic:
        channel.topic = channel_data.topic
    
    # Обновление admin_id по admin_email
    if channel_data.admin_email:
        admin = db.query(User).filter(User.email == channel_data.admin_email).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin with this email not found")
        channel.admin_id = admin.id

    # Обновление moderator_id по moderator_email
    if channel_data.moderator_email:
        moderator = db.query(User).filter(User.email == channel_data.moderator_email).first()
        if not moderator:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Moderator with this email not found")
        channel.moderator_id = moderator.id

    db.commit()
    db.refresh(channel)
    
    return {"message": "Channel updated successfully", "channel": channel}
