from pydantic import BaseModel, EmailStr
from typing import Optional

class ChannelCreate(BaseModel):
    name: str
    is_private: bool = False
    topic: Optional[str] = None
    admin_email: Optional[EmailStr] = None
    moderator_email: Optional[EmailStr] = None
