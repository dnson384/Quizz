from uuid import UUID
from pydantic import BaseModel
from typing import List, Literal, Optional


class DTOPracticeTestOutput(BaseModel):
    practice_test_id: UUID
    practice_test_name: str
    author_avatar_url: str
    author_username: str


class DTOQuestion(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str


class DTOQuestionOptions(BaseModel):
    option_id: UUID
    option_text: str
    is_correct: bool


class DTOPracticeTestQuestions(BaseModel):
    question: DTOQuestion
    options: List[DTOQuestionOptions]


class DTOPracticeTestDetailOutput(BaseModel):
    practice_test: DTOPracticeTestOutput
    questions: List[DTOPracticeTestQuestions]


# Lịch sử làm bài kiểm tra
class DTOResultOutput(BaseModel):
    result_id: UUID
    num_of_questions: int
    score: int


class DTOHistoryOutput(BaseModel):
    history_id: UUID
    option_id: List[UUID | None]
    question_detail: DTOPracticeTestQuestions


class DTOResultWithPracticeTest(BaseModel):
    result: DTOResultOutput
    base_info: DTOPracticeTestOutput


class DTOResultWithHistory(BaseModel):
    result: DTOResultOutput
    base_info: DTOPracticeTestOutput
    histories: List[DTOHistoryOutput]


# Thêm
class DTOBaseInfoInput(BaseModel):
    practice_test_name: str
    user_id: UUID


class DTOQuestionBaseInput(BaseModel):
    question_text: str
    question_type: Literal["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]


class DTOAnswerOptionsInput(BaseModel):
    option_text: str
    is_correct: bool


class DTOQuestionInput(BaseModel):
    question: DTOQuestionBaseInput
    options: List[DTOAnswerOptionsInput]


class DTONewPracticeTestInput(BaseModel):
    base_info: DTOBaseInfoInput
    questions: List[DTOQuestionInput]


# Submit test
class DTOAnsweredQuestion(BaseModel):
    question_id: UUID
    option_id: Optional[List[UUID]]


class DTOSubmitTestInput(BaseModel):
    practice_test_id: UUID
    answer_questions: List[DTOAnsweredQuestion]
    num_of_questions: int
    score: int


# Sửa
class DTOUpdateBaseInfoInput(BaseModel):
    practice_test_name: str


class DTOUpdateQuestionBaseInput(BaseModel):
    question_text: str
    question_type: Literal["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]


class DTOUpdateOptionInput(BaseModel):
    option_id: Optional[UUID]
    option_text: str
    is_correct: bool


class DTOUpdateQuestionInput(BaseModel):
    question_id: Optional[UUID]
    question: Optional[DTOUpdateQuestionBaseInput]
    options: List[DTOUpdateOptionInput]


class DTOUpdatePracticeTestInput(BaseModel):
    base_info: Optional[DTOUpdateBaseInfoInput]
    questions: List[DTOUpdateQuestionInput]


# Xoá
class DTODeleteOptions(BaseModel):
    question_id: UUID
    option_id: UUID
