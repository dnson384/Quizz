import re
from uuid import UUID
from uuid6 import uuid7
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class LoginMethod(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"


class User:
    def __init__(
        self,
        _user_id: UUID,
        _username: str,
        _email: str,
        _role: str,
        _login_method: str,
        _avatar_url: str,
        _is_actived: bool,
        _created_at: datetime,
        _updated_at: datetime,
    ):
        if not EMAIL_REGEX.match(_email):
            raise ValueError("Email không đúng định dạng hoặc bị bỏ trống")
        if _role not in ["ADMIN", "STUDENT", "TEACHER"]:
            raise ValueError("Vai trò không hợp lệ")
        if _login_method not in ["EMAIL", "GOOGLE"]:
            raise ValueError("Phương thức đăng nhập không hợp lệ")

        self._user_id = _user_id
        self._username = _username
        self._email = _email
        self._role = _role
        self._login_method = _login_method
        self._avatar_url = _avatar_url
        self._is_actived = _is_actived
        self._created_at = _created_at
        self._updated_at = _updated_at

    @classmethod
    def create_new_user(
        cls,
        username: str,
        email: str,
        role: str,
        login_method: str,
        avatar_url: str = "/static/avatars/owl.jpg",
    ) -> "User":
        return cls(
            _user_id=uuid7(),
            _username=username,
            _email=email,
            _role=role,
            _login_method=login_method,
            _avatar_url=avatar_url,
            _is_actived=True,
            _created_at=datetime.utcnow(),
            _updated_at=datetime.utcnow(),
        )

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> str:
        return self._role

    @property
    def login_method(self) -> str:
        return self._login_method

    @property
    def avatar_url(self) -> str:
        return self._avatar_url

    @property
    def is_actived(self) -> str:
        return self._is_actived

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at


@dataclass(frozen=True)
class UserOutput:
    user_id: UUID
    email: str
    username: str
    role: UserRole
    avatar_url: str
    login_method: str
    is_actived: bool


@dataclass(frozen=True)
class NewUserEmailInput:
    email: str
    username: str
    hashed_password: str
    role: UserRole
    login_method: LoginMethod


@dataclass(frozen=True)
class LoginUserEmailInput:
    email: str
    plain_password: str


@dataclass(frozen=True)
class UpdateUserInput:
    email: Optional[str]
    username: Optional[str]
    role: Optional[UserRole]
    avatar_url: Optional[str]
