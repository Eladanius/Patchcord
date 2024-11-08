"""
Purpose: The reaction model stores information about user reactions to messages, such as emoticons or likes.

Why you need it: This model allows users to respond quickly to messages by adding emojis or another type of reaction to them. Reactions help to maintain informal and interactive communication in the chat.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base

class Reaction(Base):
    __tablename__ = 'reactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    emoji = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    message = relationship("Message", back_populates="reactions")
    user = relationship("User", back_populates="reactions")
