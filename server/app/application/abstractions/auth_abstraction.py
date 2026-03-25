from abc import ABC, abstractmethod
from typing import Dict

from app.domain.entities.user.user_entity import (
    NewUserEmailInput,
    LoginUserEmailInput,
    User,
)


class IAuthService(ABC):
    @abstractmethod
    def register_user_email(self, user_in: NewUserEmailInput):
        pass

    @abstractmethod
    def login_user_email(self, user_in: LoginUserEmailInput) -> Dict:
        pass

    @abstractmethod
    def logout_user(self, refresh_token: str) -> bool:
        pass

    @abstractmethod
    def validate_access_token(self, access_token: str) -> Dict:
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> Dict:
        pass
