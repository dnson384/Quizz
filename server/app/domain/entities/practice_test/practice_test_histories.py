from uuid import UUID
from uuid6 import uuid7
from typing import Optional, List
from dataclasses import dataclass

from .practice_test_question_entity import QuestionWithOptionsOutput


class PracticeTestHistory:
    def __init__(
        self,
        _history_id: UUID,
        _result_id: UUID,
        _question_id: UUID,
        _option_id: Optional[UUID],
    ):
        self._history_id = _history_id
        self._result_id = _result_id
        self._question_id = _question_id
        self._option_id = _option_id

    @classmethod
    def create_new_history(
        cls,
        result_id: UUID,
        question_id: UUID,
        option_id: Optional[UUID],
    ) -> "PracticeTestHistory":
        return cls(
            _history_id=uuid7(),
            _result_id=result_id,
            _question_id=question_id,
            _option_id=option_id,
        )

    @property
    def history_id(self) -> UUID:
        return self._history_id

    @property
    def result_id(self) -> UUID:
        return self._result_id

    @property
    def question_id(self) -> UUID:
        return self._question_id

    @property
    def option_id(self) -> Optional[UUID]:
        return self._option_id


@dataclass(frozen=True)
class HistoryInput:
    question_id: UUID
    option_id: Optional[UUID]


@dataclass(frozen=True)
class HistoryOutput:
    history_id: UUID
    option_id: List[UUID]
    question_detail: QuestionWithOptionsOutput


@dataclass(frozen=True)
class QuestionHistory:
    question_id: UUID
    history: HistoryOutput
