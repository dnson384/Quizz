from pydantic import BaseModel
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"


class LoginMethod(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"


class DTOUserCreate(BaseModel):
    email: str
    username: str
    plain_password: str
    role: UserRole
    login_method: LoginMethod


# Schema đăng nhập
class DTOLoginEmail(BaseModel):
    email: str
    plain_password: str


class DTOUserOutput(BaseModel):
    user_id: UUID
    email: str
    username: str
    role: UserRole
    avatar_url: str
    login_method: str


class DTOLoginSuccessResponse(BaseModel):
    user: DTOUserOutput
    access_token: str
    refresh_token: str
