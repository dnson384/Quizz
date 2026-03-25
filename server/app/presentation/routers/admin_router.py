from fastapi import Depends, APIRouter, status, Request, File, UploadFile
from uuid import UUID
from typing import List

from app.presentation.controllers.admin_controller import AdminController
from app.presentation.schemas.user_schema import UserOut, CurrentUser
from app.presentation.dependencies.dependencies import (
    get_admin_controller,
    get_current_user,
)

router = APIRouter(prefix="/admin", tags=["ADMIN"])


@router.get("/all-users", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_all_users(
    current_user: CurrentUser = Depends(get_current_user),
    controller: AdminController = Depends(get_admin_controller),
):
    user_id = current_user.user_id
    role = current_user.role.value
    return controller.get_all_users(user_id, role)


@router.put("/grant-admin", response_model=bool, status_code=status.HTTP_200_OK)
def grant_admin(
    user_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    controller: AdminController = Depends(get_admin_controller),
):
    return controller.grant_admin(current_user.user_id, current_user.role, user_id)


@router.put("/lock-user", response_model=bool, status_code=status.HTTP_200_OK)
def lock_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    controller: AdminController = Depends(get_admin_controller),
):
    return controller.lock_user(current_user.user_id, current_user.role, user_id)


@router.put("/unlock-user", response_model=bool, status_code=status.HTTP_200_OK)
def unlock_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    controller: AdminController = Depends(get_admin_controller),
):
    return controller.unlock_user(current_user.user_id, current_user.role, user_id)
