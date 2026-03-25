from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.domain.entities.user.user_entity import (
    UserOutput,
    NewUserEmailInput,
    UpdateUserInput,
)
from app.domain.entities.user.user_email_entity import UserEmailOutput


class IUserRepository(ABC):
    @abstractmethod
    def get_all_users(self) -> List[UserOutput]:
        pass

    @abstractmethod
    def create_new_user_email(self, user_in: NewUserEmailInput) -> UserOutput:
        pass

    @abstractmethod
    def get_user_email_auth(self, id: str) -> UserEmailOutput:
        pass

    @abstractmethod
    def check_user_email_existed(self, email: str):
        pass

    @abstractmethod
    def get_user_by_id(self, id: str) -> UserOutput:
        pass

    @abstractmethod
    def update_user_by_id(self, id: UUID, payload: UpdateUserInput) -> UserOutput:
        pass

    @abstractmethod
    def grant_admin(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def lock_user(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def unlock_user(self, id: UUID) -> bool:
        pass
