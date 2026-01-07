from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    age: int
    email: EmailStr


class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
