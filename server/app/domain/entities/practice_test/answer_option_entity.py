from uuid import UUID
from uuid6 import uuid7
from dataclasses import dataclass


class AnswerOption:
    def __init__(
        self, _option_id: UUID, _question_id: UUID, _option_text: str, _is_correct: bool
    ):
        if not _question_id:
            raise ValueError("Không có câu hỏi")
        AnswerOption.validate_option(_option_text, _is_correct)

        self._option_id = _option_id
        self._question_id = _question_id
        self._option_text = _option_text
        self._is_correct = _is_correct

    @classmethod
    def create_new_answer_option(
        cls,
        question_id: UUID,
        option_text: str,
        is_correct: bool,
    ) -> "AnswerOption":
        return cls(
            _option_id=uuid7(),
            _question_id=question_id,
            _option_text=option_text,
            _is_correct=is_correct,
        )

    @property
    def option_id(self) -> UUID:
        return self._option_id

    @property
    def question_id(self) -> UUID:
        return self._question_id

    @property
    def option_text(self) -> str:
        return self._option_text

    @property
    def is_correct(self) -> bool:
        return self._is_correct

    def change_option(self, new_option_text: str | None, new_is_correct: bool):
        option_text_to_check = (
            new_option_text if new_option_text is not None else self._option_text
        )
        is_correct_to_check = (
            new_is_correct if new_is_correct is not None else self._is_correct
        )

        try:
            self.validate_option(option_text_to_check, is_correct_to_check)
        except ValueError as e:
            raise ValueError(f"Cập nhật không hợp lệ: {e}")

        if new_option_text is not None and new_option_text != self._option_text:
            self._option_text = new_option_text
        if new_is_correct is not None and new_is_correct != self._is_correct:
            self._is_correct = new_is_correct

    @staticmethod
    def validate_option(_option_text: str, _is_correct: bool):
        if not _option_text:
            raise ValueError("Không có câu trả lời")
        if _is_correct is None:
            raise ValueError("Câu trả lời không có đúng sai")


@dataclass(frozen=True)
class AnswerOptionOutput:
    option_id: UUID
    option_text: str
    is_correct: bool


@dataclass(frozen=True)
class NewAnswerOptionInput:
    option_text: str
    is_correct: bool


@dataclass(frozen=True)
class UpdateAnswerOptionInput:
    option_id: UUID
    option_text: str
    is_correct: bool

@dataclass(frozen=True)
class DeleteOption:
    question_id: UUID
    option_id: UUID