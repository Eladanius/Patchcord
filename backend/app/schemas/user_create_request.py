from pydantic import BaseModel, EmailStr, SecretStr

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr