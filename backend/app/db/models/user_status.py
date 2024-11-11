"""
Purpose: The user status model stores data about the current user status (for example, online or offline).

Why you need it: This model allows you to display the user's status to other users (for example, "online", "busy") 
and update it in real time. This helps other users understand if their contacts are available.
"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base

class UserStatus(Base):
    __tablename__ = 'user_statuses'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    status_color = Column(String, nullable=True)