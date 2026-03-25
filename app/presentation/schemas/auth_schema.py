from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class LoginMethod(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"


# Schema đăng ký
class UserCreateEmail(BaseModel):
    email: str
    username: str
    plain_password: str
    role: UserRole


# Schema đăng nhập
class UserLoginEmail(BaseModel):
    email: EmailStr
    plain_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
    role: str | None = None
