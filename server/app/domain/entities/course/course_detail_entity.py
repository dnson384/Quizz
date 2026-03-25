from uuid import UUID
from uuid6 import uuid7
from dataclasses import dataclass


class CourseDetail:
    def __init__(
        self,
        _course_detail_id: UUID,
        _course_id: UUID,
        _term: str,
        _definition: str,
    ):
        if not _course_id:
            raise ValueError("Không có học phần")

        CourseDetail.validate_content(_term, _definition)

        self._course_detail_id = _course_detail_id
        self._course_id = _course_id
        self._term = _term
        self._definition = _definition

    @classmethod
    def create_new_course_detail(
        cls, course_id: UUID, term: str, definition: str
    ) -> "CourseDetail":
        return cls(
            _course_detail_id=uuid7(),
            _course_id=course_id,
            _term=term,
            _definition=definition,
        )

    @property
    def course_detail_id(self) -> UUID:
        return self._course_detail_id

    @property
    def course_id(self) -> UUID:
        return self._course_id

    @property
    def term(self) -> str:
        return self._term

    @property
    def definition(self) -> str:
        return self._definition

    def update_course_detail(self, new_term: str = None, new_definition: str = None):
        term_to_check = new_term if new_term is not None else self._term
        def_to_check = (
            new_definition if new_definition is not None else self._definition
        )

        try:
            self.validate_content(term_to_check, def_to_check)
        except ValueError as e:
            raise ValueError(f"Cập nhật không hợp lệ: {e}")

        if new_term is not None and new_term != self._term:
            self._term = new_term

        if new_definition is not None and new_definition != self._definition:
            self._definition = new_definition

    @staticmethod
    def validate_content(term: str, definition: str):
        if not term:
            raise ValueError("Không có thuật ngữ")
        if not definition:
            raise ValueError("Không có định nghĩa")

@dataclass(frozen=True)
class CourseDetailOutput:
    course_detail_id: str
    term: str
    definition: str

@dataclass(frozen=True)
class CreateNewCourseDetailInput:
    term: str
    definition: str

@dataclass(frozen=True)
class UpdateCourseDetailInput:
    course_detail_id: UUID
    term: str
    definition: str