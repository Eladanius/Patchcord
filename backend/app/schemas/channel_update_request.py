from pydantic import BaseModel, EmailStr
from typing import Optional

class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    topic: Optional[str] = None
    admin_email: Optional[EmailStr] = None
    moderator_email: Optional[EmailStr] = None
