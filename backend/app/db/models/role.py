"""
Purpose: The role model describes which roles exist in the application and what rights they grant.

Why you need it: The role model allows you to create a rights system to limit or provide access to various functions
(for example, sending messages, deleting messages, adding users to the channel). This allows the administrator or moderator to manage the channel or users.
"""

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(String, nullable=False)
