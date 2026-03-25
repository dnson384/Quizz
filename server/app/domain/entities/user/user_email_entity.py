from uuid import UUID
from dataclasses import dataclass


class UserEmail:
    def __init__(
        self,
        _user_id: UUID,
        _hashed_password: str,
    ):
        if not _user_id:
            raise ValueError("Không có người dùng")
        if not _hashed_password:
            raise ValueError("Mật khẩu không được để trống")

        self._user_id = _user_id
        self._hashed_password = _hashed_password

    @classmethod
    def create_new_user_email(
        cls,
        user_id: UUID,
        hashed_password: str,
    ) -> "UserEmail":
        return cls(
            _user_id=user_id,
            _hashed_password=hashed_password,
        )

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def hashed_password(self) -> str:
        return self._hashed_password


@dataclass(frozen=True)
class UserEmailOutput:
    user_id: UUID
    hashed_password: str
