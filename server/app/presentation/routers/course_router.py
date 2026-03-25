from fastapi import APIRouter, Depends, status, Body
from uuid import UUID
from typing import List

from app.presentation.controllers.course_controller import CourseController
from app.presentation.schemas.course_schema import (
    CourseOutput,
    CourseWithDetailsOutput,
    CourseQuestionOutput,
    NewCourseInput,
    NewCourseDetailInput,
    UpdateCourseRequest,
)
from app.presentation.schemas.user_schema import CurrentUser
from app.presentation.dependencies.dependencies import (
    get_course_controller,
    get_current_user,
)

router = APIRouter(prefix="/course", tags=["COURSE"])


@router.get(
    "/my-course", response_model=List[CourseOutput], status_code=status.HTTP_200_OK
)
def get_user_course(
    current_user: CurrentUser = Depends(get_current_user),
    controller: CourseController = Depends(get_course_controller),
):
    user_id = current_user.user_id
    return controller.get_user_course(user_id)


@router.get(
    "/random", response_model=List[CourseOutput], status_code=status.HTTP_200_OK
)
def get_random_courses(controller: CourseController = Depends(get_course_controller)):
    return controller.get_random_course()


@router.get("/", response_model=CourseWithDetailsOutput, status_code=status.HTTP_200_OK)
def get_coures_detail_by_id(
    course_id: UUID, controller: CourseController = Depends(get_course_controller)
):
    result = controller.get_course_detail_by_id(course_id=course_id)
    return CourseWithDetailsOutput(
        course=result.get("course"), course_detail=result.get("course_detail")
    )


@router.get(
    "/learn", response_model=CourseQuestionOutput, status_code=status.HTTP_200_OK
)
def get_course_learn_by_id(
    course_id: str, controller: CourseController = Depends(get_course_controller)
):
    return controller.get_course_learn_by_id(course_id)


@router.get(
    "/test", response_model=CourseQuestionOutput, status_code=status.HTTP_200_OK
)
def get_course_test_by_id(
    course_id: str, controller: CourseController = Depends(get_course_controller)
):
    return controller.get_course_test_by_id(course_id)


@router.post("/", response_model=bool, status_code=status.HTTP_201_CREATED)
def create_new_course(
    course_in: NewCourseInput,
    detail_in: List[NewCourseDetailInput],
    current_user: CurrentUser = Depends(get_current_user),
    controller: CourseController = Depends(get_course_controller),
):
    print(detail_in)
    user_id = current_user.user_id
    return controller.create_new_course(user_id, course_in, detail_in)


@router.put(
    "/{course_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
def update_course(
    course_id: UUID,
    payload: UpdateCourseRequest,
    current_user: CurrentUser = Depends(get_current_user),
    controller: CourseController = Depends(get_course_controller),
):
    user_id = current_user.user_id
    return controller.update_course(user_id, course_id, payload)


@router.delete(
    "/{course_id}/detail",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
def delete_course_detail(
    course_id: UUID,
    course_detail_id: List[UUID] = Body(..., embed=True),
    current_user: CurrentUser = Depends(get_current_user),
    controller: CourseController = Depends(get_course_controller),
):
    user_id = current_user.user_id
    return controller.delete_course_detail(user_id, course_id, course_detail_id)


@router.delete("/{course_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_course(
    course_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    controller: CourseController = Depends(get_course_controller),
):
    user_id = current_user.user_id
    return controller.delete_course(user_id, course_id)
