from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.course_repo import CoursesRepository
from app.infrastructure.database.repositories.practice_test_repo import (
    PracticeTestRepository,
)
from app.infrastructure.database.repositories.user_repo import UserRepository
from app.infrastructure.database.repositories.refresh_token_repo import (
    RefreshTokenRepository,
)

from app.infrastructure.config.security_service_impl import SecurityServiceImpl
from app.application.abstractions.security_abstraction import ISecurityService

from sqlalchemy.orm import Session
from fastapi import Depends


def get_course_repo(db: Session = Depends(get_db)) -> CoursesRepository:
    return CoursesRepository(db)


def get_practice_test_repo(db: Session = Depends(get_db)) -> PracticeTestRepository:
    return PracticeTestRepository(db)


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_refresh_token_repo(db: Session = Depends(get_db)) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)


def get_security_service() -> ISecurityService:
    return SecurityServiceImpl()
