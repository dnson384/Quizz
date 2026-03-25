from fastapi import Depends, APIRouter, status, Request, File, UploadFile

from app.presentation.controllers.user_controller import UserController
from app.presentation.schemas.user_schema import UserOut, UpdateUserInput, CurrentUser
from app.presentation.dependencies.dependencies import (
    get_user_controller,
    get_current_user,
)

router = APIRouter(prefix="/user", tags=["USER"])


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_me(req: Request, controller: UserController = Depends(get_user_controller)):
    access_token = req.headers["Authorization"].split(" ")[-1]
    return controller.get_access_user(access_token=access_token)


@router.post("/upload-avatar", status_code=status.HTTP_200_OK)
def upload_avatar(
    file: UploadFile = File(...),
    controller: UserController = Depends(get_user_controller),
):
    return controller.upload_temp_avatar(file)


@router.put("/update-me", response_model=bool, status_code=status.HTTP_200_OK)
def update_me(
    payload: UpdateUserInput,
    current_user: CurrentUser = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller),
):
    user_id = current_user.user_id
    return controller.update_me(user_id, payload)
