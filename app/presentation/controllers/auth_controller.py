from fastapi import status, HTTPException


from app.application.services.auth_service import AuthService
from app.application.dtos.auth_dto import (
    DTOUserCreate,
    DTOLoginEmail,
    DTOLoginSuccessResponse,
)
from app.application.exceptions import (
    EmailExistedError,
    InvalidCredentialsError,
    AccountNotFoundError,
    AccoutHasBeenLocked,
)

from app.presentation.schemas.user_schema import UserOut, UserResponse
from app.presentation.schemas.auth_schema import UserCreateEmail, UserLoginEmail


class AuthController:
    def __init__(self, service: AuthService):
        self.service = service

    def register_user_email(self, user_in: UserCreateEmail):
        register_dto = DTOUserCreate(
            email=user_in.email,
            username=user_in.username,
            plain_password=user_in.plain_password,
            role=user_in.role,
            login_method="EMAIL",
        )
        try:
            new_user = self.service.register_user_email(register_dto)
            return UserOut(
                user_id=new_user.user_id,
                email=new_user.email,
                username=user_in.username,
                role=user_in.role,
                avatar_url=new_user.avatar_url,
            )
        except EmailExistedError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def login_user_email(self, user_in: UserLoginEmail) -> UserResponse:
        try:
            user_auth: DTOLoginSuccessResponse = self.service.login_user_email(
                DTOLoginEmail(
                    email=user_in.email, plain_password=user_in.plain_password
                )
            )
            return UserResponse(
                user=UserOut(
                    user_id=user_auth.user.user_id,
                    username=user_auth.user.username,
                    email=user_auth.user.email,
                    role=user_auth.user.role,
                    avatar_url=user_auth.user.avatar_url,
                ),
                access_token=user_auth.access_token,
                refresh_token=user_auth.refresh_token,
            )
        except AccoutHasBeenLocked as e:
            raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=str(e))
        except InvalidCredentialsError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    def logout_user(self, refresh_token: str):
        try:
            return self.service.logout_user(refresh_token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Đã xảy ra lỗi không mong muốn.",
            )

    def re_generate_access_token(self, refresh_token: str):
        try:
            return self.service.refresh_access_token(refresh_token)
        except InvalidCredentialsError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except AccountNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
