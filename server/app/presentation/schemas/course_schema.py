from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, TypedDict, Optional


class CourseOutput(BaseModel):
    course_id: UUID
    course_name: str
    author_avatar_url: str
    author_username: str
    author_role: str
    num_of_terms: int

    model_config = ConfigDict(from_attributes=True)


class CourseDetailOutput(BaseModel):
    course_detail_id: UUID
    term: str
    definition: str

    model_config = ConfigDict(from_attributes=True)


class CourseWithDetailsOutput(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class LearnQuestionOutput(TypedDict):
    question: CourseDetailOutput
    options: List[CourseDetailOutput]


class CourseQuestionOutput(TypedDict):
    course: CourseOutput
    questions: List[LearnQuestionOutput]


# Tạo mới
class NewCourseInput(BaseModel):
    course_name: str


class NewCourseDetailInput(BaseModel):
    term: str
    definition: str


# Sửa
class UpdateCourseInput(BaseModel):
    course_name: str


class UpdateCourseDetailInput(BaseModel):
    course_detail_id: UUID | None
    term: str
    definition: str


class UpdateCourseRequest(BaseModel):
    course: Optional[UpdateCourseInput] = None
    details: List[UpdateCourseDetailInput]
