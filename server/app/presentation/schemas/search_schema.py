from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import List


class SearchInput(BaseModel):
    keyword: str = Field()
    type: str = Field(default="all")
    cursor_id: str | None = Field(default=None)


class CourseOutput(BaseModel):
    course_id: UUID
    course_name: str
    author_avatar_url: str
    author_username: str
    author_role: str
    num_of_terms: int

    model_config = ConfigDict(from_attributes=True)


class PracticeTestOutput(BaseModel):
    practice_test_id: UUID
    author_username: str
    practice_test_name: str

    model_config = ConfigDict(from_attributes=True)


class SearchOutput(BaseModel):
    courses: List[CourseOutput]
    practice_tests: List[PracticeTestOutput]
