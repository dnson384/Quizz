from fastapi import status, HTTPException
from uuid import UUID
from typing import List

from app.application.services.course_service import CourseService
from app.application.dtos.course_dto import (
    DTONewCourseInput,
    DTONewCourseDetailInput,
    DTOCourseWithDetails,
    DTOUpdateCourseInput,
    DTOUpdateCourseDetailInput,
    DTOUpdateCourseRequest,
    DTOCourseOutput,
)
from app.application.exceptions import (
    CourseNotFoundError,
    UserNotFoundError,
    UserNotAllowError,
    CourseDetailNotFoundError,
)

from app.presentation.schemas.course_schema import (
    CourseQuestionOutput,
    CourseWithDetailsOutput,
    LearnQuestionOutput,
    CourseOutput,
    CourseDetailOutput,
    NewCourseInput,
    NewCourseDetailInput,
    UpdateCourseRequest,
)


class CourseController:
    def __init__(self, service: CourseService):
        self.service = service

    def get_user_course(self, user_id: UUID):
        try:
            courses: List[DTOCourseOutput] = self.service.get_user_course(user_id)
            return [
                CourseOutput(
                    course_id=course.course_id,
                    course_name=course.course_name,
                    author_avatar_url=course.author_avatar_url,
                    author_username=course.author_username,
                    author_role=course.author_role,
                    num_of_terms=course.num_of_terms,
                )
                for course in courses
            ]
        except CourseNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def get_random_course(self):
        try:
            return self.service.get_random_course()
        except CourseNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_course_detail_by_id(self, course_id: UUID):
        try:
            response = self.service.get_course_detail_by_id(course_id=course_id)
            return CourseWithDetailsOutput(
                course=response.get("course"),
                course_detail=response.get("course_detail"),
            )
        except CourseNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def get_course_learn_by_id(self, course_id: str):
        try:
            response = self.service.get_course_learn_by_id(course_id)
            course = response.course
            questions = response.questions
            course_res = CourseOutput(
                course_id=course.course_id,
                course_name=course.course_name,
                author_avatar_url=course.author_avatar_url,
                author_username=course.author_username,
                author_role=course.author_role,
                num_of_terms=course.num_of_terms,
            )
            questions_res: List[LearnQuestionOutput] = []
            for question in questions:
                questions_res.append(
                    LearnQuestionOutput(
                        question=question.question,
                        options=question.options,
                    )
                )
            return CourseQuestionOutput(course=course_res, questions=questions_res)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_course_test_by_id(self, course_id: str):
        try:
            response = self.service.get_course_test_by_id(course_id)
            course = response.course
            questions = response.questions
            course_res = CourseOutput(
                course_id=course.course_id,
                course_name=course.course_name,
                author_avatar_url=course.author_avatar_url,
                author_username=course.author_username,
                author_role=course.author_role,
                num_of_terms=course.num_of_terms,
            )
            questions_res: List[LearnQuestionOutput] = []
            for question in questions:
                questions_res.append(
                    LearnQuestionOutput(
                        question=question.question,
                        options=question.options,
                    )
                )
            return CourseQuestionOutput(course=course_res, questions=questions_res)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def create_new_course(
        self,
        user_id: UUID,
        course_in: NewCourseInput,
        detail_in: List[NewCourseDetailInput],
    ):
        try:
            course_in_dto = DTONewCourseInput(
                course_name=course_in.course_name, user_id=user_id
            )

            detail_in_dto: List[DTONewCourseDetailInput] = []
            for detail in detail_in:
                detail_in_dto.append(
                    DTONewCourseDetailInput(
                        term=detail.term, definition=detail.definition
                    )
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

        try:
            self.service.create_new_course(course_in_dto, detail_in_dto)
            return True
        except UserNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def update_course(
        self, user_id: UUID, course_id: UUID, payload: UpdateCourseRequest
    ):
        try:
            return self.service.update_course(
                user_id=user_id,
                course_id=course_id,
                payload=DTOUpdateCourseRequest(
                    course=(
                        DTOUpdateCourseInput(course_name=payload.course.course_name)
                        if payload.course
                        else None
                    ),
                    details=[
                        DTOUpdateCourseDetailInput(
                            course_detail_id=detail.course_detail_id,
                            term=detail.term,
                            definition=detail.definition,
                        )
                        for detail in payload.details
                    ],
                ),
            )
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except CourseNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_course_detail(
        self, user_id: UUID, course_id: UUID, course_detail_id: List[UUID]
    ):
        try:
            return self.service.delete_course_detail(
                user_id, course_id, course_detail_id
            )
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except CourseNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except CourseDetailNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_course(self, user_id: UUID, course_id: UUID):
        try:
            return self.service.delete_course(user_id, course_id)
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except CourseNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
