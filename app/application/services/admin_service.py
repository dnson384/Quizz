from uuid import UUID

from app.domain.exceptions.user_exceptions import UserNotFoundErrorDomain

from app.application.abstractions.refresh_token_abstraction import (
    IRefreshTokenRepository,
)
from app.application.abstractions.user_abstraction import IUserRepository
from app.application.dtos.user_dto import DTOUserOutput
from app.application.exceptions import UserNotAllowError, UserNotFoundError


class AdminServices:
    def __init__(self, user_repo: IUserRepository, token_repo: IRefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def get_all_users(self, user_id: UUID, role: str):
        if role != "ADMIN":
            raise UserNotAllowError

        cur_user = self.user_repo.get_user_by_id(user_id)
        if cur_user.role != "ADMIN":
            raise UserNotAllowError

        users_domain = self.user_repo.get_all_users()

        return [
            DTOUserOutput(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                role=user.role,
                avatar_url=user.avatar_url,
                login_method=user.login_method,
                is_actived=user.is_actived,
            )
            for user in users_domain
        ]

    def grant_admin(self, admin_id: UUID, user_id: UUID):
        current_admin = self.user_repo.get_user_by_id(admin_id)
        if current_admin.role != "ADMIN":
            raise UserNotAllowError

        try:
            if self.user_repo.grant_admin(user_id):
                return self.token_repo.revoke_all_tokens_for_user(user_id)
        except UserNotFoundErrorDomain:
            raise UserNotFoundError

    def lock_user(self, admin_id: UUID, user_id: UUID):
        current_admin = self.user_repo.get_user_by_id(admin_id)
        if current_admin.role != "ADMIN":
            raise UserNotAllowError
        
        try:
            if self.user_repo.lock_user(user_id):
                return self.token_repo.revoke_all_tokens_for_user(user_id)
        except UserNotFoundErrorDomain:
            raise UserNotFoundError
        
        
    def unlock_user(self, admin_id: UUID, user_id: UUID):
        current_admin = self.user_repo.get_user_by_id(admin_id)
        if current_admin.role != "ADMIN":
            raise UserNotAllowError
        
        try:
            if self.user_repo.unlock_user(user_id):
                return self.token_repo.revoke_all_tokens_for_user(user_id)
        except UserNotFoundErrorDomain:
            raise UserNotFoundError