from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.infrastructure.database.connection import Base


class CourseModel(Base):
    __tablename__ = "courses"

    course_id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    course_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course_detail = relationship(
        "CourseDetailModel",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    course_user = relationship("UserModel", back_populates="user_course")


class CourseDetailModel(Base):
    __tablename__ = "course_details"

    course_detail_id = Column(UUID(as_uuid=True), primary_key=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id"))
    term = Column(String(255), nullable=False)
    definition = Column(Text, nullable=False)

    course = relationship("CourseModel", back_populates="course_detail")
