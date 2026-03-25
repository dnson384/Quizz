import random
from uuid import UUID
from typing import List, TypedDict

from app.domain.entities.course.course_entity import (
    CreateNewCourseInput,
    CourseOutput,
    UpdateCourseInput,
)
from app.domain.entities.course.course_detail_entity import (
    CreateNewCourseDetailInput,
    CourseDetailOutput,
    UpdateCourseDetailInput,
)
from app.domain.exceptions.course_exception import (
    CoursesNotFoundErrorDomain,
    CourseDetailsNotFoundErrorDomain,
)

from app.application.abstractions.course_abstraction import ICourseRepository
from app.application.abstractions.user_abstraction import IUserRepository
from app.application.dtos.course_dto import (
    DTONewCourseDetailInput,
    DTONewCourseInput,
    DTOCourseOutput,
    DTOTestQuestion,
    DTOCourseTestOutput,
    DTOCourseDetailOutput,
    DTOCourseWithDetails,
    DTOUpdateCourseRequest,
)
from app.application.exceptions import (
    UserNotAllowError,
    UserNotFoundError,
    CourseNotFoundError,
    CourseDetailNotFoundError,
)


class CourseWithDetailsResponse(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class CourseService:
    def __init__(self, course_repo: ICourseRepository, user_repo: IUserRepository):
        self.course_repo = course_repo
        self.user_repo = user_repo

    def get_user_course(self, user_id: UUID):
        try:
            courses: List[CourseOutput] = self.course_repo.get_courses_by_user_id(
                user_id
            )
            return [
                DTOCourseOutput(
                    course_id=course.course_id,
                    course_name=course.course_name,
                    author_avatar_url=course.author_avatar_url,
                    author_username=course.author_username,
                    author_role=course.author_role,
                    num_of_terms=course.num_of_terms,
                )
                for course in courses
            ]
        except CoursesNotFoundErrorDomain as e:
            raise CourseNotFoundError(str(e))

    def get_random_course(self):
        try:
            sample_courses = self.course_repo.get_random_courses()

            if not sample_courses:
                raise CourseNotFoundError("Không có học phần")

            return sample_courses
        except Exception as e:
            raise Exception("Không thể lấy ngẫu nhiên học phần", e)

    def get_course_detail_by_id(self, course_id: UUID):
        try:
            course_detail_result: CourseWithDetailsResponse = (
                self.course_repo.get_course_detail_by_id(course_id=course_id)
            )

            return course_detail_result
        except CoursesNotFoundErrorDomain as e:
            raise CourseNotFoundError(str(e))

    def create_question(
        self,
        current_term: CourseDetailOutput,
        course_detail: List[CourseDetailOutput],
    ):
        pool: List[CourseDetailOutput] = [
            item for item in course_detail if item != current_term
        ]
        random_items: List[CourseDetailOutput] = random.sample(pool, 3)

        current_term_dto = DTOCourseDetailOutput(
            course_detail_id=current_term.course_detail_id,
            term=current_term.term,
            definition=current_term.definition,
        )
        random_items_dto: List[DTOCourseDetailOutput] = [
            DTOCourseDetailOutput(
                course_detail_id=item.course_detail_id,
                term=item.term,
                definition=item.definition,
            )
            for item in random_items
        ]

        return DTOTestQuestion(question=current_term_dto, options=random_items_dto)

    def get_course_learn_by_id(self, course_id: str):
        try:
            response = self.get_course_detail_by_id(course_id)
            course = response.get("course")
            course_detail = response.get("course_detail")

            questions: List[DTOTestQuestion] = list(
                map(
                    lambda current_course: self.create_question(
                        current_course, course_detail
                    ),
                    course_detail,
                )
            )
            course_dto: DTOCourseOutput = DTOCourseOutput(
                course_id=course.course_id,
                course_name=course.course_name,
                author_avatar_url=course.author_avatar_url,
                author_username=course.author_username,
                author_role=course.author_role,
                num_of_terms=course.num_of_terms,
            )

            return DTOCourseTestOutput(course=course_dto, questions=questions)
        except Exception as e:
            raise Exception("Không thể tạo tính năng học", e)

    def get_course_test_by_id(self, course_id: str):
        try:
            response = self.get_course_detail_by_id(course_id)
            course = response.get("course")
            course_detail = response.get("course_detail")

            num_of_questions = 20 if len(course_detail) >= 20 else len(course_detail)
            course_detail_random: List[CourseDetailOutput] = random.sample(
                course_detail, num_of_questions
            )
            questions: List[DTOTestQuestion] = list(
                map(
                    lambda current_term: self.create_question(
                        current_term, course_detail_random
                    ),
                    course_detail_random,
                )
            )
            course_dto: DTOCourseOutput = DTOCourseOutput(
                course_id=course.course_id,
                course_name=course.course_name,
                author_avatar_url=course.author_avatar_url,
                author_username=course.author_username,
                author_role=course.author_role,
                num_of_terms=course.num_of_terms,
            )
            return DTOCourseTestOutput(course=course_dto, questions=questions)
        except Exception as e:
            raise Exception("Không thể tạo tính năng kiểm tra", e)

    def create_new_course(
        self,
        course_in: DTONewCourseInput,
        detail_in: List[DTONewCourseDetailInput],
    ):
        try:
            if not self.user_repo.get_user_by_id(course_in.user_id):
                raise UserNotFoundError(
                    f"User with ID {course_in.user_id} does not exist"
                )

            course_in_domain = CreateNewCourseInput(
                course_name=course_in.course_name, user_id=course_in.user_id
            )
            detail_in_domain: List[CreateNewCourseDetailInput] = []
            for detail in detail_in:
                detail_in_domain.append(
                    CreateNewCourseDetailInput(
                        term=detail.term, definition=detail.definition
                    )
                )

            return self.course_repo.create_new_course(
                course_in_domain, detail_in_domain
            )
        except Exception as e:
            raise Exception("Không thể thêm mới học phần - service", e)

    def check_user_course(self, user_id: UUID, course_id: UUID):
        try:
            if not self.course_repo.check_user_course(user_id, course_id):
                raise UserNotAllowError()
        except CoursesNotFoundErrorDomain as e:
            raise CourseNotFoundError(str(e))

    def update_course(
        self, user_id: UUID, course_id: UUID, payload: DTOUpdateCourseRequest
    ):
        self.check_user_course(user_id, course_id)

        try:
            if payload.course:
                self.course_repo.update_course(
                    course_id=course_id,
                    course_in=UpdateCourseInput(course_name=payload.course.course_name),
                )
        except Exception as e:
            raise Exception("Lỗi khi cập nhật tên học phần", e)

        try:
            for detail in payload.details:
                if detail.course_detail_id:
                    self.course_repo.update_course_detail(
                        course_id=course_id,
                        detail_in=UpdateCourseDetailInput(
                            course_detail_id=detail.course_detail_id,
                            term=detail.term,
                            definition=detail.definition,
                        ),
                    )

                else:
                    self.course_repo.create_new_course_detail(
                        course_id=course_id,
                        detail_in=UpdateCourseDetailInput(
                            course_detail_id=detail.course_detail_id,
                            term=detail.term,
                            definition=detail.definition,
                        ),
                    )
        except Exception as e:
            raise Exception("Lỗi khi cập nhật chi tiết học phần", e)
        return True

    def delete_course_detail(
        self, user_id: UUID, course_id: UUID, course_detail_id: List[UUID]
    ) -> bool:
        self.check_user_course(user_id, course_id)
        return self.course_repo.delete_course_detail(course_id, course_detail_id)

    def delete_course(self, user_id: UUID, course_id: UUID):
        self.check_user_course(user_id, course_id)
        return self.course_repo.delete_course(course_id)
