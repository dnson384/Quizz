from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from dataclasses import asdict

from app.domain.entities.user.user_entity import (
    User,
    NewUserEmailInput,
    UserOutput,
    UpdateUserInput,
)
from app.domain.entities.user.user_email_entity import UserEmail, UserEmailOutput
from app.domain.exceptions.user_exceptions import UserNotFoundErrorDomain

from app.infrastructure.database.models.user_model import UserModel, UserEmailModel

from app.application.abstractions.user_abstraction import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[UserOutput]:
        users = self.db.query(UserModel).filter(UserModel.role != "ADMIN").all()
        return [
            UserOutput(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                role=user.role,
                avatar_url=user.avatar_url,
                login_method=user.login_method,
                is_actived=user.is_actived,
            )
            for user in users
        ]

    def create_new_user_email(self, user_in: NewUserEmailInput) -> UserOutput:
        new_user_domain = User.create_new_user(
            email=user_in.email,
            username=user_in.username,
            role=user_in.role,
            login_method=user_in.login_method,
        )
        new_user_model = UserModel(
            user_id=new_user_domain.user_id,
            username=new_user_domain.username,
            email=new_user_domain.email,
            role=new_user_domain.role,
            login_method=new_user_domain.login_method,
            avatar_url=new_user_domain.avatar_url,
            created_at=new_user_domain.created_at,
            updated_at=new_user_domain.updated_at,
        )
        new_user_email_domain = UserEmail.create_new_user_email(
            user_id=new_user_domain.user_id, hashed_password=user_in.hashed_password
        )
        new_user_email_model = UserEmailModel(
            user_id=new_user_email_domain.user_id,
            hashed_password=new_user_email_domain.hashed_password,
        )

        self.db.add(new_user_model)
        self.db.add(new_user_email_model)

        self.db.commit()
        self.db.refresh(new_user_model)
        return UserOutput(
            user_id=new_user_model.user_id,
            email=new_user_model.email,
            username=new_user_model.username,
            role=new_user_model.role,
            avatar_url=new_user_model.avatar_url,
            login_method=new_user_domain.login_method,
            is_actived=new_user_domain.is_actived,
        )

    def get_user_email_auth(self, id: str) -> UserEmailOutput:
        query = (
            self.db.query(UserEmailModel).filter(UserEmailModel.user_id == id).first()
        )
        return UserEmailOutput(
            user_id=query.user_id, hashed_password=query.hashed_password
        )

    def check_user_email_existed(self, email: str) -> Optional[UserOutput]:
        query = self.db.query(UserModel).filter(UserModel.email == email).first()
        if query:
            return UserOutput(
                user_id=query.user_id,
                email=query.email,
                username=query.username,
                role=query.role,
                avatar_url=query.avatar_url,
                login_method=query.login_method,
                is_actived=query.is_actived,
            )
        return None

    def get_user_by_id(self, id: str) -> UserOutput:
        user = self.db.query(UserModel).filter(UserModel.user_id == id).first()
        return UserOutput(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
            avatar_url=user.avatar_url,
            login_method=user.login_method,
            is_actived=user.is_actived,
        )

    def update_user_by_id(self, id: UUID, payload: UpdateUserInput):
        cur_user = self.db.query(UserModel).filter(UserModel.user_id == id).first()

        if not cur_user:
            raise UserNotFoundErrorDomain("Người dùng không tồn tại")

        update_data = {key: value for key, value in asdict(payload).items() if value}

        for key, value in update_data.items():
            setattr(cur_user, key, value)

        self.db.commit()
        return True

    def grant_admin(self, id: UUID) -> bool:
        user = self.db.query(UserModel).filter(UserModel.user_id == id).first()
        if not user:
            raise UserNotFoundErrorDomain

        user.role = "ADMIN"
        self.db.commit()
        return True

    def lock_user(self, id: UUID) -> bool:
        user = self.db.query(UserModel).filter(UserModel.user_id == id).first()
        if not user:
            raise UserNotFoundErrorDomain

        user.is_actived = False
        self.db.commit()
        return True

    def unlock_user(self, id: UUID) -> bool:
        user = self.db.query(UserModel).filter(UserModel.user_id == id).first()
        if not user:
            raise UserNotFoundErrorDomain

        user.is_actived = True
        self.db.commit()
        return True
