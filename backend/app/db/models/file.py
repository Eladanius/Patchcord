"""
Purpose: The file model stores information about downloaded files, such as images and documents, that can be attached to messages.

Why you need it: This model is needed to track all files uploaded by users and link these files to specific messages. This can be useful for managing storage and simplifying access to media files.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base

class File(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_url = Column(String, nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'), nullable=True)
