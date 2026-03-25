from pydantic import BaseModel, ConfigDict
from typing import List, Literal, Optional
from uuid import UUID


class PracticeTestOutput(BaseModel):
    practice_test_id: UUID
    practice_test_name: str
    author_avatar_url: str
    author_username: str

    model_config = ConfigDict(from_attributes=True)


class Question(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str

    model_config = ConfigDict(from_attributes=True)


class QuestionOptions(BaseModel):
    option_id: UUID
    option_text: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)


class PracticeTestQuestions(BaseModel):
    question: Question
    options: List[QuestionOptions]

    model_config = ConfigDict(from_attributes=True)


class PracticeTestDetailOutput(BaseModel):
    practice_test: PracticeTestOutput
    questions: List[PracticeTestQuestions]

    model_config = ConfigDict(from_attributes=True)


# Lịch sử
class ResultOutput(BaseModel):
    result_id: UUID
    num_of_questions: int
    score: int


class HistoryOutput(BaseModel):
    history_id: UUID
    option_id: List[UUID | None]
    question_detail: PracticeTestQuestions


class ResultWithPracticeTest(BaseModel):
    result: ResultOutput
    base_info: PracticeTestOutput


class ResultWithHistory(BaseModel):
    result: ResultOutput
    base_info: PracticeTestOutput
    histories: List[HistoryOutput]


# Thêm
class BaseInfoInput(BaseModel):
    practice_test_name: str


class QuestionBaseInput(BaseModel):
    question_text: str
    question_type: Literal["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]


class AnswerOptionsInput(BaseModel):
    option_text: str
    is_correct: bool


class QuestionInput(BaseModel):
    question: QuestionBaseInput
    options: List[AnswerOptionsInput]


class NewPracticeTestInput(BaseModel):
    base_info: BaseInfoInput
    questions: List[QuestionInput]


# Submit test
class AnsweredQuestion(BaseModel):
    question_id: UUID
    option_id: Optional[List[UUID]]


class SubmitTestInput(BaseModel):
    practice_test_id: UUID
    answer_questions: List[AnsweredQuestion]
    num_of_questions: int
    score: int


# Sửa
class UpdateBaseInfoInput(BaseModel):
    practice_test_name: str


class UpdateQuestionBaseInput(BaseModel):
    question_text: str
    question_type: Literal["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]


class UpdateOptionInput(BaseModel):
    option_id: Optional[UUID]
    option_text: str
    is_correct: bool


class UpdateQuestionInput(BaseModel):
    question_id: Optional[UUID]
    question: Optional[UpdateQuestionBaseInput]
    options: List[UpdateOptionInput]


class UpdatePracticeTestInput(BaseModel):
    base_info: Optional[UpdateBaseInfoInput]
    questions: List[UpdateQuestionInput]


# Xoá
class DeleteOptions(BaseModel):
    question_id: UUID
    option_id: UUID
