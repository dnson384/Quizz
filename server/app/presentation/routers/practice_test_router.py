from fastapi import APIRouter, Depends, status, Body
from uuid import UUID
from typing import List, Optional

from app.presentation.controllers.practice_test_controller import PracticeTestController
from app.presentation.schemas.practice_test_schema import (
    PracticeTestOutput,
    PracticeTestDetailOutput,
    ResultWithPracticeTest,
    ResultWithHistory,
    # Tạo
    NewPracticeTestInput,
    SubmitTestInput,
    # Sửa
    UpdatePracticeTestInput,
    # Xoá
    DeleteOptions,
)
from app.presentation.schemas.user_schema import CurrentUser
from app.presentation.dependencies.dependencies import (
    get_practice_test_controller,
    get_current_user,
)

router = APIRouter(prefix="/practice-test", tags=["PRACTICETEST"])


@router.get(
    "/my-practice-tests",
    response_model=List[PracticeTestOutput],
    status_code=status.HTTP_200_OK,
)
def get_user_practice_test(
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.get_user_practice_test(user_id)


@router.get(
    "/random",
    response_model=List[PracticeTestOutput],
    status_code=status.HTTP_200_OK,
)
def get_random_courses(
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_random_practice_test()


@router.get(
    "/", response_model=PracticeTestDetailOutput, status_code=status.HTTP_200_OK
)
def get_detail(
    practice_test_id: str,
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_practice_test_detail_by_id(practice_test_id=practice_test_id)


@router.get(
    "/random-questions",
    response_model=PracticeTestDetailOutput,
    status_code=status.HTTP_200_OK,
)
def getrandom_questions(
    practice_test_id: UUID,
    count: Optional[int] = None,
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_random_questions_by_id(practice_test_id, count)


@router.get(
    "/history",
    response_model=List[ResultWithPracticeTest],
    status_code=status.HTTP_200_OK,
)
def get_all_histories(
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.get_all_histories(user_id)


@router.get(
    "/history/{practice_test_id}",
    response_model=ResultWithHistory,
    status_code=status.HTTP_200_OK,
)
def get_practice_test_history(
    practice_test_id: UUID,
    result_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.get_practice_test_history(user_id, result_id, practice_test_id)


@router.post("/", response_model=bool, status_code=status.HTTP_201_CREATED)
def create_new_practice_test(
    payload: NewPracticeTestInput,
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.create_new_practice_test(user_id, payload)


@router.post("/submit-test", response_model=UUID, status_code=status.HTTP_201_CREATED)
def create_test_result(
    payload: SubmitTestInput,
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.submit_test(user_id, payload)


@router.put("/{practice_test_id}", response_model=bool, status_code=status.HTTP_200_OK)
def update_practice_test(
    practice_test_id: UUID,
    payload: UpdatePracticeTestInput,
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.update_practice_test(user_id, practice_test_id, payload)


@router.delete(
    "/{practice_test_id}/options",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
def delete_option(
    practice_test_id: UUID,
    payload: List[DeleteOptions],
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.delete_option(user_id, practice_test_id, payload)


@router.delete(
    "/{practice_test_id}/questions",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
def delete_question(
    practice_test_id: UUID,
    question_id: List[UUID] = Body(..., embed=True),
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.delete_question(user_id, practice_test_id, question_id)


@router.delete(
    "/{practice_test_id}", response_model=bool, status_code=status.HTTP_200_OK
)
def delete_practice_test(
    practice_test_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    user_id = current_user.user_id
    return controller.delete_practice_test(user_id, practice_test_id)
