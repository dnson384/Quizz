from uuid import UUID

from app.domain.entities.practice_test.practice_test_entity import (
    PracticeTest,
    NewBaseInfoInput,
    UpdateBaseInfoInput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    PracticeTestQuestion,
    NewQuestionBaseInput,
)
from app.domain.entities.practice_test.answer_option_entity import (
    AnswerOption,
    NewAnswerOptionInput,
)
from app.domain.entities.practice_test.practice_test_results_entity import (
    PracticeTestResult,
    ResultInput,
)
from app.domain.entities.practice_test.practice_test_histories import (
    PracticeTestHistory,
    HistoryInput,
)

from app.infrastructure.database.models.practice_test_model import (
    PracticeTestModel,
    PracticeTestQuestionModel,
    AnswerOptionModel,
    PracticeTestResultModel,
    PracticeTestHistoryModel,
)


class Mapper:
    def new_practice_test_domain(payload: NewBaseInfoInput) -> PracticeTest:
        return PracticeTest.create_new_practice_test(
            user_id=payload.user_id,
            practice_test_name=payload.practice_test_name,
        )

    def new_question_domain(
        practice_test_id: UUID, payload: NewQuestionBaseInput
    ) -> PracticeTestQuestion:
        domain = PracticeTestQuestion.create_new_question(
            practice_test_id=practice_test_id,
            question_text=payload.question_text,
            question_type=payload.question_type,
        )
        return domain

    def new_option_domain(
        quesiton_id: UUID, payload: NewAnswerOptionInput
    ) -> AnswerOption:
        return AnswerOption.create_new_answer_option(
            question_id=quesiton_id,
            option_text=payload.option_text,
            is_correct=payload.is_correct,
        )

    def new_result_domain(user_id: UUID, result: ResultInput) -> PracticeTestResult:
        return PracticeTestResult.create_new_practice_test_result(
            user_id=user_id,
            practice_test_id=result.practice_test_id,
            num_of_questions=result.num_of_questions,
            score=result.score,
        )

    def new_history_domain(
        result_id: UUID, history: HistoryInput
    ) -> PracticeTestHistory:
        return PracticeTestHistory.create_new_history(
            result_id=result_id,
            question_id=history.question_id,
            option_id=history.option_id,
        )

    def practice_test_domain_to_model(domain: PracticeTest) -> PracticeTestModel:
        return PracticeTestModel(
            practice_test_id=domain.practice_test_id,
            user_id=domain.user_id,
            practice_test_name=domain.practice_test_name,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    def question_domain_to_model(
        domain: PracticeTestQuestion,
    ) -> PracticeTestQuestionModel:
        return PracticeTestQuestionModel(
            question_id=domain.question_id,
            practice_test_id=domain.practice_test_id,
            question_text=domain.question_text,
            question_type=domain.question_type,
        )

    def option_domain_to_model(
        domain: AnswerOption,
    ) -> AnswerOptionModel:
        return AnswerOptionModel(
            option_id=domain.option_id,
            question_id=domain.question_id,
            option_text=domain.option_text,
            is_correct=domain.is_correct,
        )

    def practice_test_result_domain_to_model(
        domain: PracticeTestResult,
    ) -> PracticeTestResultModel:
        return PracticeTestResultModel(
            result_id=domain.result_id,
            user_id=domain.user_id,
            practice_test_id=domain.practice_test_id,
            num_of_questions=domain.num_of_questions,
            score=domain.score,
        )

    def practice_test_history_domain_to_model(
        domain: PracticeTestHistory,
    ) -> PracticeTestHistoryModel:
        return PracticeTestHistoryModel(
            history_id=domain.history_id,
            result_id=domain.result_id,
            question_id=domain.question_id,
            option_id=domain.option_id,
        )
