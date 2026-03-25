from fastapi import Depends, Request, HTTPException, status
from uuid import UUID

from app.application.services.search_service import SearchServices
from app.application.services.auth_service import AuthService
from app.application.services.user_service import UserServices
from app.application.services.course_service import CourseService
from app.application.services.practice_test_service import PracticeTestService
from app.application.services.admin_service import AdminServices

from app.presentation.controllers.search_controller import SearchController
from app.presentation.controllers.auth_controller import AuthController
from app.presentation.controllers.user_controller import UserController
from app.presentation.controllers.course_controller import CourseController
from app.presentation.controllers.practice_test_controller import PracticeTestController
from app.presentation.controllers.admin_controller import AdminController

from app.application.abstractions.course_abstraction import ICourseRepository
from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.application.abstractions.user_abstraction import IUserRepository
from app.application.abstractions.refresh_token_abstraction import (
    IRefreshTokenRepository,
)
from app.application.abstractions.security_abstraction import ISecurityService
from app.application.abstractions.auth_abstraction import IAuthService

from app.infrastructure.config.dependencies import (
    get_course_repo,
    get_practice_test_repo,
    get_user_repo,
    get_refresh_token_repo,
    get_security_service,
)

from app.presentation.schemas.user_schema import CurrentUser


def get_search_service(
    course_repo: ICourseRepository = Depends(get_course_repo),
    practice_test_repo: IPracticeTestRepository = Depends(get_practice_test_repo),
):
    return SearchServices(course_repo, practice_test_repo)


def get_search_controller(
    service: SearchServices = Depends(get_search_service),
) -> SearchController:
    return SearchController(service)


def get_auth_service(
    user_repo: IUserRepository = Depends(get_user_repo),
    token_repo: IRefreshTokenRepository = Depends(get_refresh_token_repo),
    security_service: ISecurityService = Depends(get_security_service),
) -> AuthService:
    return AuthService(user_repo, token_repo, security_service)


def get_auth_controller(
    service: AuthService = Depends(get_auth_service),
) -> AuthController:
    return AuthController(service)


def get_user_service(
    user_repo: IUserRepository = Depends(get_user_repo),
    auth_service: IAuthService = Depends(get_auth_service),
) -> UserServices:
    return UserServices(user_repo, auth_service)


def get_user_controller(
    service: UserController = Depends(get_user_service),
) -> UserController:
    return UserController(service)


def get_course_service(
    course_repo: ICourseRepository = Depends(get_course_repo),
    user_repo: IUserRepository = Depends(get_user_repo),
) -> CourseService:
    return CourseService(course_repo, user_repo)


def get_course_controller(
    service: CourseService = Depends(get_course_service),
) -> CourseController:
    return CourseController(service)


def get_practice_test_service(
    practice_test_repo: IPracticeTestRepository = Depends(get_practice_test_repo),
) -> PracticeTestService:
    return PracticeTestService(practice_test_repo)


def get_practice_test_controller(
    service: PracticeTestService = Depends(get_practice_test_service),
) -> PracticeTestController:
    return PracticeTestController(service)


def get_admin_service(
    user_repo: IUserRepository = Depends(get_user_repo),
    token_repo: IRefreshTokenRepository = Depends(get_refresh_token_repo),
) -> AdminServices:
    return AdminServices(user_repo, token_repo)


def get_admin_controller(service: AdminServices = Depends(get_admin_service)):
    return AdminController(service)


def get_current_user(
    req: Request, controller: UserController = Depends(get_user_controller)
) -> CurrentUser:
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Không tìm thấy token"
        )
    token = authorization.split(" ")[-1]

    try:
        cur_user = controller.get_access_user(token)
        return CurrentUser(user_id=cur_user.user_id, role=cur_user.role)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
