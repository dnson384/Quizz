from dataclasses import dataclass
from typing import List, TypedDict, Optional
from uuid import UUID

from app.domain.entities.practice_test.practice_test_entity import (
    NewBaseInfoInput,
    UpdateBaseInfoInput,
    PracticeTestOutput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    NewQuestionBaseInput,
    UpdateQuestionBaseInput,
)
from app.domain.entities.practice_test.answer_option_entity import (
    NewAnswerOptionInput,
    UpdateAnswerOptionInput,
    DeleteOption,
)
from app.domain.entities.practice_test.practice_test_results_entity import (
    ResultInput,
    ResultWithHistory,
    ResultWithPracticeTest,
)
from app.domain.entities.practice_test.practice_test_histories import HistoryInput
from app.domain.exceptions.practice_test_exception import (
    PracticeTestsNotFoundErrorDomain,
    ResultNotFoundErrorDomain,
    UserNotAllowThisResultErrorDomain,
)

from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.application.dtos.practice_test_dto import (
    DTOPracticeTestOutput,
    DTOQuestion,
    DTOQuestionOptions,
    DTOPracticeTestQuestions,
    # Lịch sử làm bài
    DTOResultOutput,
    DTOHistoryOutput,
    DTOResultWithPracticeTest,
    DTOResultWithHistory,
    # Thêm
    DTONewPracticeTestInput,
    DTOSubmitTestInput,
    DTOUpdatePracticeTestInput,
    DTODeleteOptions,
)
from app.application.exceptions import (
    UserNotAllowError,
    PracticeTestsNotFoundError,
    ResultNotFoundError,
    UserNotAllowThisResultError,
)


@dataclass(frozen=True)
class NewQuestionInput:
    question: NewQuestionBaseInput
    options: List[NewAnswerOptionInput]


@dataclass(frozen=True)
class NewPracticeTestInput:
    base_info: NewBaseInfoInput
    questions: List[NewQuestionInput]


@dataclass(frozen=True)
class UpdateQuestionInput:
    question_id: Optional[UUID]
    question_base: UpdateQuestionBaseInput
    options: UpdateAnswerOptionInput


class PracticeTestService:
    def __init__(self, practice_test_repo: IPracticeTestRepository):
        self.practice_test_repo = practice_test_repo

    def get_user_practice_test(self, user_id: UUID):
        try:
            practice_tests: List[PracticeTestOutput] = (
                self.practice_test_repo.get_practice_tests_by_user_id(user_id)
            )
            return [
                DTOPracticeTestOutput(
                    practice_test_id=practice_test.practice_test_id,
                    practice_test_name=practice_test.practice_test_name,
                    author_avatar_url=practice_test.author_avatar_url,
                    author_username=practice_test.author_username,
                )
                for practice_test in practice_tests
            ]
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))

    def get_random_practice_test(self):
        try:
            sample_practice_tests = self.practice_test_repo.get_random_practice_test()

            if not sample_practice_tests:
                raise PracticeTestsNotFoundError("Không có bài kiểm tra thử")

            return sample_practice_tests
        except Exception as e:
            raise Exception("Không thể lấy ngẫu nhiên bài kiểm tra thử", e)

    def get_practice_test_detail_by_id(self, practice_test_id: str):
        try:
            return self.practice_test_repo.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id
            )
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))
        except Exception as e:
            raise Exception("Không thể lấy thông tin chi tiết bài kiểm tra thử", e)

    def get_random_questions_by_id(self, practice_test_id: str, count: int | None):
        try:
            return self.practice_test_repo.get_practice_test_random_detail_by_id(
                practice_test_id=practice_test_id, count=count
            )
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))
        except Exception as e:
            raise Exception("Không thể lấy thông tin chi tiết bài kiểm tra thử", e)

    def get_all_histories(self, user_id: UUID):
        response: List[ResultWithPracticeTest] = (
            self.practice_test_repo.get_all_histories(user_id)
        )

        dto_response: List[DTOResultWithPracticeTest] = []
        for raw in response:
            result_domain = raw.result
            base_info_domain = raw.base_info

            result_domain = DTOResultOutput(
                result_id=result_domain.result_id,
                num_of_questions=result_domain.num_of_questions,
                score=result_domain.score,
            )

            practice_test_domain = DTOPracticeTestOutput(
                practice_test_id=base_info_domain.practice_test_id,
                practice_test_name=base_info_domain.practice_test_name,
                author_avatar_url=base_info_domain.author_avatar_url,
                author_username=base_info_domain.author_username,
            )

            dto_response.append(
                DTOResultWithPracticeTest(
                    result=result_domain, base_info=practice_test_domain
                )
            )
        return dto_response

    def get_practice_test_history(
        self, user_id: UUID, result_id: UUID, practice_test_id: UUID
    ):
        try:
            response: ResultWithHistory = (
                self.practice_test_repo.get_practice_test_history(
                    user_id, result_id, practice_test_id
                )
            )
            dto_result = DTOResultOutput(
                result_id=response.result.result_id,
                num_of_questions=response.result.num_of_questions,
                score=response.result.score,
            )
            dto_base_info = DTOPracticeTestOutput(
                practice_test_id=response.base_info.practice_test_id,
                practice_test_name=response.base_info.practice_test_name,
                author_avatar_url=response.base_info.author_avatar_url,
                author_username=response.base_info.author_username,
            )

            dto_histories: List[DTOHistoryOutput] = []
            for history in response.histories:
                question_detail = history.history.question_detail
                dto_question_base = DTOQuestion(
                    question_id=question_detail.question_id,
                    question_text=question_detail.question_text,
                    question_type=question_detail.question_type,
                )
                dto_options = [
                    DTOQuestionOptions(
                        option_id=option.option_id,
                        option_text=option.option_text,
                        is_correct=option.is_correct,
                    )
                    for option in question_detail.options
                ]
                dto_histories.append(
                    DTOHistoryOutput(
                        history_id=history.history.history_id,
                        option_id=history.history.option_id,
                        question_detail=DTOPracticeTestQuestions(
                            question=dto_question_base, options=dto_options
                        ),
                    ),
                )

            return DTOResultWithHistory(
                result=dto_result, base_info=dto_base_info, histories=dto_histories
            )
        except UserNotAllowThisResultErrorDomain:
            raise UserNotAllowThisResultError
        except PracticeTestsNotFoundErrorDomain:
            raise PracticeTestsNotFoundError
        except ResultNotFoundErrorDomain:
            raise ResultNotFoundError

    def create_new_practice_test(self, payload: DTONewPracticeTestInput):
        base_info_domain = NewBaseInfoInput(
            practice_test_name=payload.base_info.practice_test_name,
            user_id=payload.base_info.user_id,
        )

        questions_domain: List[NewQuestionInput] = []
        for question_payload in payload.questions:
            question_domain = NewQuestionBaseInput(
                question_text=question_payload.question.question_text,
                question_type=question_payload.question.question_type,
            )

            options_domain: List[NewAnswerOptionInput] = [
                NewAnswerOptionInput(
                    option_text=option_payload.option_text,
                    is_correct=option_payload.is_correct,
                )
                for option_payload in question_payload.options
            ]

            questions_domain.append(
                NewQuestionInput(question=question_domain, options=options_domain)
            )

        return self.practice_test_repo.create_new_practice_test(
            payload=NewPracticeTestInput(
                base_info=base_info_domain, questions=questions_domain
            )
        )

    def submit_test(self, user_id: UUID, payload: DTOSubmitTestInput):
        resutl_domain = ResultInput(
            user_id=user_id,
            practice_test_id=payload.practice_test_id,
            num_of_questions=payload.num_of_questions,
            score=payload.score,
        )

        history_domain: List[HistoryInput] = []
        for answered in payload.answer_questions:
            if answered.option_id:
                for option_id in answered.option_id:
                    history_domain.append(
                        HistoryInput(
                            question_id=answered.question_id, option_id=option_id
                        )
                    )
            else:
                history_domain.append(
                    HistoryInput(question_id=answered.question_id, option_id=None)
                )

        return self.practice_test_repo.submit_test(
            user_id, resutl_domain, history_domain
        )

    def check_valid_practice_test(self, user_id: UUID, practice_test_id: UUID):
        try:
            if not self.practice_test_repo.check_user_practice_test(
                user_id, practice_test_id
            ):
                raise UserNotAllowError()
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))

    def update_practice_test(
        self, user_id: UUID, practice_test_id: UUID, payload: DTOUpdatePracticeTestInput
    ):
        self.check_valid_practice_test(user_id, practice_test_id)

        base_info_domain = (
            UpdateBaseInfoInput(practice_test_name=payload.base_info.practice_test_name)
            if payload.base_info
            else None
        )

        questions_update_domain: List[UpdateQuestionInput] = []
        questions_create_domain: List[UpdateQuestionInput] = []
        for question_payload in payload.questions:
            question_id = question_payload.question_id
            question_base_domain = (
                UpdateQuestionBaseInput(
                    question_text=question_payload.question.question_text,
                    question_type=question_payload.question.question_type,
                )
                if question_payload.question
                else None
            )
            options_domain: List[UpdateAnswerOptionInput] = [
                UpdateAnswerOptionInput(
                    option_id=option_payload.option_id,
                    option_text=option_payload.option_text,
                    is_correct=option_payload.is_correct,
                )
                for option_payload in question_payload.options
            ]
            if question_id:
                questions_update_domain.append(
                    UpdateQuestionInput(
                        question_id=question_id,
                        question_base=question_base_domain,
                        options=options_domain,
                    )
                )
            else:
                questions_create_domain.append(
                    UpdateQuestionInput(
                        question_id=None,
                        question_base=question_base_domain,
                        options=options_domain,
                    )
                )

        return self.practice_test_repo.update_practice_test(
            practice_test_id,
            base_info_domain,
            questions_create_domain,
            questions_update_domain,
        )

    def delete_option(
        self, user_id: UUID, practice_test_id: UUID, payload: List[DTODeleteOptions]
    ):
        self.check_valid_practice_test(user_id, practice_test_id)
        return self.practice_test_repo.delete_answer_option(
            practice_test_id,
            [
                DeleteOption(question_id=dto.question_id, option_id=dto.option_id)
                for dto in payload
            ],
        )

    def delete_question(
        self, user_id: UUID, practice_test_id: UUID, question_id: List[UUID]
    ):
        self.check_valid_practice_test(user_id, practice_test_id)
        return self.practice_test_repo.delete_question(practice_test_id, question_id)

    def delete_practice_test(self, user_id: UUID, practice_test_id: UUID):
        self.check_valid_practice_test(user_id, practice_test_id)
        return self.practice_test_repo.delete_practice_test(practice_test_id)
