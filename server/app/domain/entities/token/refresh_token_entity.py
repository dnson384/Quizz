from uuid import UUID
from uuid6 import uuid7
from datetime import datetime
from dataclasses import dataclass


class RefreshToken:
    def __init__(
        self, _jti: UUID, _user_id: UUID, _expires_at: datetime, _issued_at: datetime
    ):
        if not _user_id:
            raise ValueError("Không có người dùng")
        if not _expires_at or not _issued_at:
            raise ValueError("Token phải có thời hạn")

        self._jti = _jti
        self._user_id = _user_id
        self._expires_at = _expires_at
        self._issued_at = _issued_at

    @classmethod
    def create_new_refresh_token(
        cls,
        user_id: UUID,
        expires_at: datetime,
        issued_at: datetime,
    ) -> "RefreshToken":
        return cls(
            _jti=uuid7(), _user_id=user_id, _expires_at=expires_at, _issued_at=issued_at
        )

    @property
    def jti(self) -> UUID:
        return self._jti

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def issued_at(self) -> datetime:
        return self._issued_at
