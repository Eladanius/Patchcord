"""
Purpose: The channel model is a "room" or space in which users can communicate.

Why you need it: This model is needed to create and manage channels such as text chats or group chats. 
Each channel can be public or private, and different users can join it
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    is_private = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    topic = Column(String, nullable=True)

    messages = relationship("Message", back_populates="channel")
    memberships = relationship("ChannelMembership", back_populates="channel")
