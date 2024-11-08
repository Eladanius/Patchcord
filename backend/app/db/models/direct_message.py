"""
Purpose: The personal message model is used to store private messages between two users.

Why you need it: This is a separate type of messages that differs from the messages in the channel, as it is intended only for two participants. Private messages allow users to conduct private dialogues.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base

class DirectMessage(Base):
    __tablename__ = 'direct_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    content = Column(String, nullable=True)
    attachment_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
