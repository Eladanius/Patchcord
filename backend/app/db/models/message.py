"""
Purpose: The message model stores data about each sent message in the channel.

Why do you need it: This is the main model for saving chat history. 
It allows you to store text messages and attached files (for example, images), as well as link messages to channels and users.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channels.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    content = Column(String, nullable=True)
    attachment_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
    channel = relationship("Channel", back_populates="messages")
    reactions = relationship("Reaction", back_populates="message")
