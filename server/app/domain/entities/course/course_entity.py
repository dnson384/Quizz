from uuid import UUID
from uuid6 import uuid7
from datetime import datetime
from dataclasses import dataclass


class Course:
    def __init__(
        self,
        _course_id: UUID,
        _user_id: UUID,
        _course_name: str,
        _created_at: datetime,
        _updated_at: datetime,
    ):
        if not _user_id:
            raise ValueError("Không có người dùng")
        if not _course_name:
            raise ValueError("Tên học phần không được để trống")

        self._course_id = _course_id
        self._user_id = _user_id
        self._course_name = _course_name
        self._created_at = _created_at
        self._updated_at = _updated_at

    @classmethod
    def create_new_course(
        cls,
        course_name: str,
        user_id: UUID,
    ) -> "Course":
        return cls(
            _course_id=uuid7(),
            _user_id=user_id,
            _course_name=course_name,
            _created_at=datetime.utcnow(),
            _updated_at=datetime.utcnow(),
        )

    @property
    def course_id(self) -> UUID:
        return self._course_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def course_name(self) -> str:
        return self._course_name

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_course(self, new_course_name: str = None):
        if not new_course_name:
            raise ValueError("Tên học phần không được để trống")
        self._course_name = new_course_name
        self._updated_at = datetime.utcnow()


@dataclass(frozen=True)
class CourseInput:
    keyword: str
    type: str
    cursor_id: str | None


@dataclass(frozen=True)
class CourseOutput:
    course_id: UUID
    course_name: str
    author_avatar_url: str
    author_username: str
    author_role: str
    num_of_terms: int


@dataclass(frozen=True)
class CreateNewCourseInput:
    course_name: str
    user_id: UUID


@dataclass(frozen=True)
class UpdateCourseInput:
    course_name: str
