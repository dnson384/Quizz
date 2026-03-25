from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, TypedDict, Optional


class DTOCourseOutput(BaseModel):
    course_id: UUID
    course_name: str
    author_avatar_url: str
    author_username: str
    author_role: str
    num_of_terms: int


class DTOCourseDetailOutput(BaseModel):
    course_detail_id: UUID
    term: str
    definition: str


class DTOCourseWithDetails(TypedDict):
    course: DTOCourseOutput
    course_detail: List[DTOCourseDetailOutput]


class DTONewCourseInput(BaseModel):
    course_name: str
    user_id: UUID


class DTONewCourseDetailInput(BaseModel):
    term: str
    definition: str


class DTOTestQuestion(BaseModel):
    question: DTOCourseDetailOutput
    options: List[DTOCourseDetailOutput]


class DTOCourseTestOutput(BaseModel):
    course: DTOCourseOutput
    questions: List[DTOTestQuestion]


# Sửa
class DTOUpdateCourseInput(BaseModel):
    course_name: str


class DTOUpdateCourseDetailInput(BaseModel):
    course_detail_id: UUID | None
    term: str
    definition: str


class DTOUpdateCourseRequest(BaseModel):
    course: Optional[DTOUpdateCourseInput] = None
    details: List[DTOUpdateCourseDetailInput]
