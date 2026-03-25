from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, TypedDict

from app.domain.entities.course.course_entity import (
    CourseOutput,
    CreateNewCourseInput,
    UpdateCourseInput,
)
from app.domain.entities.course.course_detail_entity import (
    CourseDetailOutput,
    CreateNewCourseDetailInput,
    UpdateCourseDetailInput,
)


class CourseWithDetailsResponse(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class ICourseRepository(ABC):
    @abstractmethod
    def get_courses_by_user_id(self, user_id: UUID) -> List[CourseOutput]:
        pass

    @abstractmethod
    def get_courses_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[CourseOutput]:
        pass

    @abstractmethod
    def get_random_courses(self) -> List[CourseOutput]:
        pass

    @abstractmethod
    def check_user_course(self, user_ud: UUID, course_id: UUID):
        pass

    @abstractmethod
    def get_course_detail_by_id(self, course_id: UUID) -> CourseWithDetailsResponse:
        pass

    @abstractmethod
    def create_new_course(
        self,
        course_in: CreateNewCourseInput,
        detail_in: List[CreateNewCourseDetailInput],
    ) -> bool:
        pass

    @abstractmethod
    def create_new_course_detail(
        self, course_id: UUID, detail_in: CreateNewCourseDetailInput
    ):
        pass

    @abstractmethod
    def update_course_detail(self, course_id: UUID, detail_in: UpdateCourseDetailInput):
        pass

    @abstractmethod
    def update_course(self, course_id: UUID, course_in: UpdateCourseInput):
        pass

    @abstractmethod
    def delete_course_detail(self, course_id: UUID, course_detail_id: List[UUID]):
        pass

    @abstractmethod
    def delete_course(self, course_id: UUID):
        pass
