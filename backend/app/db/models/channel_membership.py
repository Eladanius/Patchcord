"""
Purpose: The channel participation model describes the relationship between users and channels.

Why you need it: This model allows you to track who is a member of which channel, as well as assign roles within the channel (for example, an administrator or a regular participant). It can be used to manage user rights in different channels.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base

class ChannelMembership(Base):
    __tablename__ = 'channel_memberships'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channels.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    role = Column(String, default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="channels")
    channel = relationship("Channel", back_populates="memberships")
