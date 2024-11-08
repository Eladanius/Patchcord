"""
Purpose: The user status model stores data about the current user status (for example, online or offline).

Why you need it: This model allows you to display the user's status to other users (for example, "online", "busy") 
and update it in real time. This helps other users understand if their contacts are available.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.db.database import Base

class UserStatus(Base):
    __tablename__ = 'user_status'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    status = Column(String, default="offline")
    updated_at = Column(DateTime, default=datetime.utcnow)
