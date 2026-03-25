from datetime import datetime, timezone, timedelta
from typing import Dict

from app.domain.entities.user.user_entity import (
    NewUserEmailInput,
    UserOutput,
)
from app.domain.entities.user.user_email_entity import UserEmailOutput
from app.domain.entities.token.refresh_token_entity import (
    RefreshToken,
)

from app.application.dtos.auth_dto import (
    DTOUserCreate,
    DTOLoginEmail,
    DTOUserOutput,
    DTOLoginSuccessResponse,
)
from app.application.exceptions import (
    EmailExistedError,
    InvalidCredentialsError,
    AccountNotFoundError,
    AccoutHasBeenLocked,
)
from app.application.abstractions.security_abstraction import ISecurityService
from app.application.abstractions.user_abstraction import IUserRepository
from app.application.abstractions.refresh_token_abstraction import (
    IRefreshTokenRepository,
)
from app.application.abstractions.auth_abstraction import IAuthService


class AuthService(IAuthService):
    def __init__(
        self,
        user_repo: IUserRepository,
        token_repo: IRefreshTokenRepository,
        security_service: ISecurityService,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.security_service = security_service

    def register_user_email(self, user_in: DTOUserCreate) -> DTOUserOutput:
        # Kiểm tra email tồn tại
        if self.user_repo.check_user_email_existed(user_in.email):
            raise EmailExistedError("Email đã được đăng ký")

        hashed_password = self.security_service.hash_password(user_in.plain_password)

        new_user_domain = NewUserEmailInput(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hashed_password,
            role=user_in.role,
            login_method=user_in.login_method,
        )

        new_user: UserOutput = self.user_repo.create_new_user_email(new_user_domain)
        return DTOUserOutput(
            user_id=new_user.user_id,
            email=new_user.email,
            username=user_in.username,
            role=user_in.role,
            avatar_url=new_user.avatar_url,
            login_method=new_user.login_method,
        )

    def login_user_email(self, user_in: DTOLoginEmail):
        # Kiểm tra tài khoản tồn tại
        existed_user: UserOutput = self.user_repo.check_user_email_existed(
            user_in.email
        )
        if not existed_user or existed_user.login_method != "EMAIL":
            raise InvalidCredentialsError("Email hoặc mật khẩu không chính xác")
        if not existed_user.is_actived:
            raise AccoutHasBeenLocked("Tài khoản đã bị khoá")

        # Kiểm tra mật khẩu
        user_email_auth: UserEmailOutput = self.user_repo.get_user_email_auth(
            existed_user.user_id
        )
        if not self.security_service.verify_password(
            user_in.plain_password, user_email_auth.hashed_password
        ):
            raise InvalidCredentialsError("Email hoặc mật khẩu không chính xác")

        # Tạo Access Token
        access_token_payload = {
            "sub": str(existed_user.user_id),
            "role": str(existed_user.role),
        }
        access_token = self.security_service.create_access_token(access_token_payload)

        # Tạo và lưu Refresh Token
        new_rt_domain = RefreshToken.create_new_refresh_token(
            user_id=existed_user.user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            issued_at=datetime.now(timezone.utc),
        )
        refresh_token_payload = {
            "jti": str(new_rt_domain.jti),
            "sub": str(existed_user.user_id),
            "role": str(existed_user.role),
            "exp": new_rt_domain.expires_at,
            "iat": new_rt_domain.issued_at,
        }
        refresh_token = self.security_service.create_refresh_token(
            refresh_token_payload
        )
        self.token_repo.save_refresh_token(new_rt_domain)

        return DTOLoginSuccessResponse(
            user=DTOUserOutput(
                user_id=existed_user.user_id,
                email=existed_user.email,
                username=existed_user.username,
                role=existed_user.role,
                avatar_url=existed_user.avatar_url,
                login_method=existed_user.login_method,
            ),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def logout_user(self, refresh_token) -> bool:
        payload = self.security_service.decode_refresh_token(refresh_token)
        jti = payload.get("jti")
        return self.token_repo.revoke_refresh_token(jti)

    def validate_access_token(self, access_token: str) -> Dict:
        payload = self.security_service.decode_access_token(access_token)
        return payload

    def refresh_access_token(self, refresh_token: str) -> Dict:
        payload = self.security_service.decode_refresh_token(refresh_token)

        jti = payload.get("jti")
        user_id = payload.get("sub")

        if not self.token_repo.is_jti_valid(jti):
            raise InvalidCredentialsError(
                "Refresh token đã bị thu hồi hoặc không tồn tại"
            )

        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            raise AccountNotFoundError("Tài khoản không còn tồn tại")

        new_access_token = self.security_service.create_access_token(
            {"sub": str(user.user_id), "role": user.role}
        )

        return new_access_token
