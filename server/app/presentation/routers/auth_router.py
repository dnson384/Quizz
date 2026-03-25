from fastapi import APIRouter, Depends, status, Request

from app.presentation.controllers.auth_controller import AuthController
from app.presentation.dependencies.dependencies import get_auth_controller
from app.presentation.schemas.auth_schema import UserCreateEmail, UserLoginEmail
from app.presentation.schemas.user_schema import UserResponse, UserOut


router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user_email_endpoint(
    user_in: UserCreateEmail, controller: AuthController = Depends(get_auth_controller)
):
    return controller.register_user_email(user_in=user_in)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user_email_endpoint(
    user_in: UserLoginEmail, controller: AuthController = Depends(get_auth_controller)
):
    return controller.login_user_email(user_in=user_in)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(
    req: Request, controller: AuthController = Depends(get_auth_controller)
):
    refresh_token = req.headers["Authorization"].split(" ")[-1]
    return controller.logout_user(refresh_token)


@router.post("/refresh", response_model=str, status_code=status.HTTP_200_OK)
def refresh_access_token(
    req: Request, controller: AuthController = Depends(get_auth_controller)
):
    refresh_token = req.headers["Authorization"].split(" ")[-1]
    return controller.re_generate_access_token(refresh_token)
