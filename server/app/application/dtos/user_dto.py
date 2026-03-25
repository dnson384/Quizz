from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"


class DTOUpdateUserInput(BaseModel):
    username: Optional[str]
    email: Optional[str]
    role: Optional[UserRole]
    avatar_url: Optional[str]

class DTOUserOutput(BaseModel):
    user_id: UUID
    email: str
    username: str
    role: UserRole
    avatar_url: str
    login_method: str
    is_actived: bool