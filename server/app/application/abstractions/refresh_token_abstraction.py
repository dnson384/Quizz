from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.token.refresh_token_entity import (
    RefreshToken,
)


class IRefreshTokenRepository(ABC):
    @abstractmethod
    def save_refresh_token(self, payload: RefreshToken):
        pass

    @abstractmethod
    def is_jti_valid(self, jti: UUID) -> bool:
        """
        Kiểm tra xem JTI có tồn tại và hợp lệ trong DB không.
        Đây là hàm bạn đang hỏi.
        """
        pass

    @abstractmethod
    def revoke_refresh_token(self, jti: UUID) -> bool:
        """
        Thu hồi (xóa) JTI khỏi DB khi user đăng xuất.
        """
        pass

    @abstractmethod
    def revoke_all_tokens_for_user(self, user_id: UUID) -> int:
        """
        Thu hồi tất cả token của 1 user (ví dụ: khi đổi mật khẩu).
        """
        pass
