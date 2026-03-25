from uuid import UUID
from uuid6 import uuid7
from typing import List
from dataclasses import dataclass

from .answer_option_entity import AnswerOptionOutput

class PracticeTestQuestion:
    def __init__(
        self,
        _question_id: UUID,
        _practice_test_id: UUID,
        _question_text: str,
        _question_type: str,
    ):
        if not _practice_test_id:
            raise ValueError("Không có bài kiểm tra")

        PracticeTestQuestion.validate_question(_question_text, _question_type)

        self._question_id = _question_id
        self._practice_test_id = _practice_test_id
        self._question_text = _question_text
        self._question_type = _question_type

    @classmethod
    def create_new_question(
        cls, practice_test_id: UUID, question_text: str, question_type: str
    ) -> "PracticeTestQuestion":
        if not question_type in ["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]:
            raise ValueError("Giá trị loại câu hỏi không hợp lệ")

        return cls(
            _question_id=uuid7(),
            _practice_test_id=practice_test_id,
            _question_text=question_text,
            _question_type=question_type,
        )

    @property
    def question_id(self) -> UUID:
        return self._question_id

    @property
    def practice_test_id(self) -> UUID:
        return self._practice_test_id

    @property
    def question_text(self) -> str:
        return self._question_text

    @property
    def question_type(self) -> str:
        return self._question_type

    @staticmethod
    def validate_question(question_text: str, question_type: str):
        if not question_text:
            raise ValueError("Không có câu hỏi")
        if question_type not in ["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]:
            raise ValueError("Loại câu hỏi không hợp lệ")


@dataclass(frozen=True)
class QuestionOutput:
    question_id: UUID
    question_text: str
    question_type: str

@dataclass(frozen=True)
class QuestionWithOptionsOutput:
    question_id: UUID
    question_text: str
    question_type: str
    options: List[AnswerOptionOutput]


@dataclass(frozen=True)
class NewQuestionBaseInput:
    question_text: str
    question_type: str


@dataclass(frozen=True)
class UpdateQuestionBaseInput:
    question_text: str
    question_type: str
