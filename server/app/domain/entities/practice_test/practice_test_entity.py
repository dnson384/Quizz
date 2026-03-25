from uuid import UUID
from uuid6 import uuid7
from datetime import datetime
from dataclasses import dataclass


class PracticeTest:
    def __init__(
        self,
        _practice_test_id: UUID,
        _user_id: UUID,
        _practice_test_name: str,
        _created_at: datetime,
        _updated_at: datetime,
    ):
        if not _user_id:
            raise ValueError("Không có người dùng")
        if not _practice_test_name:
            raise ValueError("Tên bài kiểm tra không được để trống")

        self._practice_test_id = _practice_test_id
        self._user_id = _user_id
        self._practice_test_name = _practice_test_name
        self._created_at = _created_at
        self._updated_at = _updated_at

    @classmethod
    def create_new_practice_test(
        cls,
        user_id: UUID,
        practice_test_name: str,
    ) -> "PracticeTest":
        return cls(
            _practice_test_id=uuid7(),
            _user_id=user_id,
            _practice_test_name=practice_test_name,
            _created_at=datetime.utcnow(),
            _updated_at=datetime.utcnow(),
        )

    @property
    def practice_test_id(self) -> UUID:
        return self._practice_test_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def practice_test_name(self) -> str:
        return self._practice_test_name

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_course(self, new_practice_test_name: str = None):
        if not new_practice_test_name:
            raise ValueError("Tên bài kiểm tra không được để trống")
        self._practice_test_name = new_practice_test_name
        self._updated_at = datetime.utcnow()


@dataclass(frozen=True)
class PracticeTestOutput:
    practice_test_id: UUID
    practice_test_name: str
    author_avatar_url: str
    author_username: str


@dataclass(frozen=True)
class NewBaseInfoInput:
    practice_test_name: str
    user_id: UUID


@dataclass(frozen=True)
class UpdateBaseInfoInput:
    practice_test_name: str
