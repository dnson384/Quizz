from uuid import UUID
from uuid6 import uuid7
from typing import List
from dataclasses import dataclass

from .practice_test_entity import PracticeTestOutput
from .practice_test_histories import QuestionHistory

class PracticeTestResult:
    def __init__(
        self,
        _result_id: UUID,
        _user_id: UUID,
        _practice_test_id: UUID,
        _num_of_questions: int,
        _score: int,
    ):
        if not _user_id:
            raise ValueError("Không có người dùng")
        if not _practice_test_id:
            raise ValueError("Không có bài kiểm tra")

        self._result_id = _result_id
        self._user_id = _user_id
        self._practice_test_id = _practice_test_id
        self._num_of_questions = _num_of_questions
        self._score = _score

    @classmethod
    def create_new_practice_test_result(
        cls, user_id: UUID, practice_test_id: UUID, num_of_questions: int, score: int
    ) -> "PracticeTestResult":
        return cls(
            _result_id=uuid7(),
            _user_id=user_id,
            _practice_test_id=practice_test_id,
            _num_of_questions=num_of_questions,
            _score=score,
        )

    @property
    def result_id(self) -> UUID:
        return self._result_id

    @property
    def practice_test_id(self) -> UUID:
        return self._practice_test_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def num_of_questions(self) -> int:
        return self._num_of_questions

    @property
    def score(self) -> int:
        return self._score


@dataclass(frozen=True)
class ResultInput:
    user_id: UUID
    practice_test_id: UUID
    num_of_questions: int
    score: int


@dataclass(frozen=True)
class ResultOutput:
    result_id: UUID
    num_of_questions: int
    score: int

@dataclass(frozen=True)
class ResultWithHistory:
    result: ResultOutput
    base_info: PracticeTestOutput
    histories: List[QuestionHistory]

@dataclass(frozen=True)
class ResultWithPracticeTest:
    result: ResultOutput
    base_info: PracticeTestOutput