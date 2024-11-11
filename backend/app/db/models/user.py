"""
Purpose: The user model stores basic information about each person registered in the system.

Why you need it: This model allows you to manage users, their authentication and profile information, 
such as avatar and status (online/offline). Users will be associated with messages, channels and roles.
"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    auth_provider = Column(String, default="local")  # "local" для стандартной регистрации, "google" для Google OAuth
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    avatar_url = Column(String, nullable=True)
    status_id = Column(Integer, ForeignKey('user_statuses.id'))
    last_status_id = Column(Integer, ForeignKey('user_statuses.id'), nullable=True)
    role = Column(String, default="user")

    channels = relationship("ChannelMembership", back_populates="user")
    messages = relationship("Message", back_populates="user")
    reactions = relationship("Reaction", back_populates="user")
    status = relationship("UserStatus", foreign_keys=[status_id])
    last_status = relationship("UserStatus", foreign_keys=[last_status_id])