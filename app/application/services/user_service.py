from uuid import UUID

from app.domain.entities.user.user_entity import UpdateUserInput
from app.domain.exceptions.auth_exceptions import AccountNotFoundError, EmailAlreadyExistsError

from app.application.abstractions.user_abstraction import IUserRepository
from app.application.abstractions.auth_abstraction import IAuthService
from app.application.dtos.user_dto import DTOUpdateUserInput, DTOUserOutput


class UserServices:
    def __init__(self, user_repo: IUserRepository, auth_service: IAuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def get_me(self, access_token: str | None):
        payload = self.auth_service.validate_access_token(access_token)

        user_id = payload.get("sub")
        cur_user = self.user_repo.get_user_by_id(id=user_id)
        if not cur_user:
            raise AccountNotFoundError("Không tìm được tài khoản người dùng")
        return DTOUserOutput(
            user_id=cur_user.user_id,
            email=cur_user.email,
            username=cur_user.username,
            role=cur_user.role,
            avatar_url=cur_user.avatar_url,
            login_method=cur_user.login_method,
            is_actived=cur_user.is_actived,
        )

    def update_me(self, user_id: UUID, payload: DTOUpdateUserInput):
        if payload.email:
            if self.user_repo.check_user_email_existed(payload.email):
                raise EmailAlreadyExistsError("Email đã tồn tại")

        return self.user_repo.update_user_by_id(
            user_id,
            UpdateUserInput(
                email=payload.email,
                username=payload.username,
                role=payload.role,
                avatar_url=payload.avatar_url,
            ),
        )