from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    CheckConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    role_check = CheckConstraint(
        role.in_(["ADMIN", "STUDENT", "TEACHER"]), name="role_check"
    )

    login_method = Column(String(20), nullable=False)
    login_method_check = CheckConstraint(
        login_method.in_(["EMAIL", "GOOGLE"]), name="login_method_check"
    )

    avatar_url = Column(Text, nullable=True)
    is_actived = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (role_check, login_method_check)

    # users_email
    email_auth = relationship("UserEmailModel", back_populates="user", uselist=False)
    # refresh_tokens
    refresh_token = relationship(
        "RefreshTokenModel", back_populates="user", cascade="all, delete-orphan"
    )
    # courses
    user_course = relationship("CourseModel", back_populates="course_user")
    # practice_tests
    user_practice_test = relationship(
        "PracticeTestModel",
        back_populates="practice_test_user",
        cascade="all, delete-orphan",
    )
    # result
    user_result = relationship(
        "PracticeTestResultModel",
        back_populates="result_user",
        cascade="all, delete-orphan",
    )


class UserEmailModel(Base):
    __tablename__ = "users_email"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    hashed_password = Column(Text, nullable=False)

    user = relationship("UserModel", back_populates="email_auth")
