from fastapi import status, HTTPException
from uuid import UUID
from typing import List


from app.application.services.practice_test_service import PracticeTestService
from app.application.dtos.practice_test_dto import (
    DTOPracticeTestOutput,
    DTOResultWithPracticeTest,
    # POST
    DTOBaseInfoInput,
    DTOQuestionBaseInput,
    DTOAnswerOptionsInput,
    DTOQuestionInput,
    DTONewPracticeTestInput,
    DTOAnsweredQuestion,
    DTOSubmitTestInput,
    # PUT
    DTOUpdateBaseInfoInput,
    DTOUpdateQuestionBaseInput,
    DTOUpdateOptionInput,
    DTOUpdateQuestionInput,
    DTOUpdatePracticeTestInput,
    # DELETE
    DTODeleteOptions,
)
from app.application.exceptions import (
    PracticeTestsNotFoundError,
    QuestionNotFoundError,
    OptionNotFoundError,
    UserNotAllowError,
    ResultNotFoundError,
    UserNotAllowThisResultError,
)

from app.presentation.schemas.practice_test_schema import (
    PracticeTestOutput,
    Question,
    QuestionOptions,
    PracticeTestQuestions,
    PracticeTestDetailOutput,
    # Lịch sử
    ResultOutput,
    HistoryOutput,
    ResultWithPracticeTest,
    ResultWithHistory,
    # Thêm
    NewPracticeTestInput,
    SubmitTestInput,
    UpdatePracticeTestInput,
    DeleteOptions,
)


class PracticeTestController:
    def __init__(self, service: PracticeTestService):
        self.service = service

    def get_user_practice_test(self, user_id: UUID):
        try:
            practiceTests: List[DTOPracticeTestOutput] = (
                self.service.get_user_practice_test(user_id)
            )
            return [
                PracticeTestOutput(
                    practice_test_id=practiceTest.practice_test_id,
                    practice_test_name=practiceTest.practice_test_name,
                    author_avatar_url=practiceTest.author_avatar_url,
                    author_username=practiceTest.author_username,
                )
                for practiceTest in practiceTests
            ]
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def get_random_practice_test(self):
        try:
            return self.service.get_random_practice_test()
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_practice_test_detail_by_id(self, practice_test_id: str):
        try:
            response = self.service.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id
            )
            practice_test = PracticeTestOutput(
                practice_test_id=response.base_info.practice_test_id,
                practice_test_name=response.base_info.practice_test_name,
                author_avatar_url=response.base_info.author_avatar_url,
                author_username=response.base_info.author_username,
            )

            questions: List[PracticeTestQuestions] = []
            for question in response.questions:
                question_data = Question(
                    question_id=question.question.question_id,
                    question_text=question.question.question_text,
                    question_type=question.question.question_type,
                )
                options_data: List[QuestionOptions] = []
                for option in question.options:
                    options_data.append(
                        QuestionOptions(
                            option_id=option.option_id,
                            option_text=option.option_text,
                            is_correct=option.is_correct,
                        )
                    )

                questions.append(
                    PracticeTestQuestions(question=question_data, options=options_data)
                )

            return PracticeTestDetailOutput(
                practice_test=practice_test, questions=questions
            )
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def get_random_questions_by_id(self, practice_test_id: str, count: int | None):
        try:
            response = self.service.get_random_questions_by_id(
                practice_test_id=practice_test_id, count=count
            )
            practice_test = PracticeTestOutput(
                practice_test_id=response.base_info.practice_test_id,
                practice_test_name=response.base_info.practice_test_name,
                author_avatar_url=response.base_info.author_avatar_url,
                author_username=response.base_info.author_username,
            )

            questions: List[PracticeTestQuestions] = []
            for question in response.questions:
                question_data = Question(
                    question_id=question.question.question_id,
                    question_text=question.question.question_text,
                    question_type=question.question.question_type,
                )
                options_data: List[QuestionOptions] = []
                for option in question.options:
                    options_data.append(
                        QuestionOptions(
                            option_id=option.option_id,
                            option_text=option.option_text,
                            is_correct=option.is_correct,
                        )
                    )

                questions.append(
                    PracticeTestQuestions(question=question_data, options=options_data)
                )

            return PracticeTestDetailOutput(
                practice_test=practice_test, questions=questions
            )
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_all_histories(self, user_id: UUID):
        dto_response: List[DTOResultWithPracticeTest] = self.service.get_all_histories(
            user_id
        )
        response: List[ResultWithPracticeTest] = []
        for raw in dto_response:
            result_domain = raw.result
            base_info_domain = raw.base_info

            result_domain = ResultOutput(
                result_id=result_domain.result_id,
                num_of_questions=result_domain.num_of_questions,
                score=result_domain.score,
            )

            practice_test_domain = PracticeTestOutput(
                practice_test_id=base_info_domain.practice_test_id,
                practice_test_name=base_info_domain.practice_test_name,
                author_avatar_url=base_info_domain.author_avatar_url,
                author_username=base_info_domain.author_username,
            )

            response.append(
                ResultWithPracticeTest(
                    result=result_domain, base_info=practice_test_domain
                )
            )
        return response

    def get_practice_test_history(
        self, user_id: UUID, result_id: UUID, practice_test_id: UUID
    ):
        try:
            response = self.service.get_practice_test_history(
                user_id, result_id, practice_test_id
            )
            result = ResultOutput(
                result_id=response.result.result_id,
                num_of_questions=response.result.num_of_questions,
                score=response.result.score,
            )
            base_info = PracticeTestOutput(
                practice_test_id=response.base_info.practice_test_id,
                practice_test_name=response.base_info.practice_test_name,
                author_avatar_url=response.base_info.author_avatar_url,
                author_username=response.base_info.author_username,
            )
            histories: List[HistoryOutput] = []
            for history in response.histories:
                question_detail = history.question_detail
                question_base = Question(
                    question_id=question_detail.question.question_id,
                    question_text=question_detail.question.question_text,
                    question_type=question_detail.question.question_type,
                )
                options = [
                    QuestionOptions(
                        option_id=option.option_id,
                        option_text=option.option_text,
                        is_correct=option.is_correct,
                    )
                    for option in question_detail.options
                ]
                histories.append(
                    HistoryOutput(
                        history_id=history.history_id,
                        option_id=history.option_id,
                        question_detail=PracticeTestQuestions(
                            question=question_base, options=options
                        ),
                    )
                )

            return ResultWithHistory(
                result=result, base_info=base_info, histories=histories
            )
        except UserNotAllowThisResultError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except PracticeTestsNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except ResultNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def create_new_practice_test(self, user_id: UUID, payload: NewPracticeTestInput):
        base_info_dto = DTOBaseInfoInput(
            practice_test_name=payload.base_info.practice_test_name,
            user_id=user_id,
        )

        questions_dto: List[DTOQuestionInput] = []
        for question_payload in payload.questions:
            question_base_dto = DTOQuestionBaseInput(
                question_text=question_payload.question.question_text,
                question_type=question_payload.question.question_type,
            )

            options_dto: List[DTOAnswerOptionsInput] = []
            for option_payload in question_payload.options:
                options_dto.append(
                    DTOAnswerOptionsInput(
                        option_text=option_payload.option_text,
                        is_correct=option_payload.is_correct,
                    )
                )

            questions_dto.append(
                DTOQuestionInput(question=question_base_dto, options=options_dto)
            )

        new_practice_test_dto = DTONewPracticeTestInput(
            base_info=base_info_dto, questions=questions_dto
        )

        try:
            return self.service.create_new_practice_test(payload=new_practice_test_dto)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def submit_test(self, user_id: UUID, payload: SubmitTestInput):
        dto_answer = [
            DTOAnsweredQuestion(
                question_id=answer.question_id,
                option_id=answer.option_id,
            )
            for answer in payload.answer_questions
        ]
        dto_submit = DTOSubmitTestInput(
            practice_test_id=payload.practice_test_id,
            answer_questions=dto_answer,
            num_of_questions=payload.num_of_questions,
            score=payload.score,
        )
        return self.service.submit_test(user_id=user_id, payload=dto_submit)

    def update_practice_test(
        self, user_id: UUID, practice_test_id: UUID, payload: UpdatePracticeTestInput
    ):
        base_info_dto = (
            DTOUpdateBaseInfoInput(
                practice_test_name=payload.base_info.practice_test_name
            )
            if payload.base_info
            else None
        )

        questions_dto: List[DTOUpdateQuestionInput] = []
        for question_payload in payload.questions:
            question_id = question_payload.question_id
            question_base_dto = (
                DTOUpdateQuestionBaseInput(
                    question_text=question_payload.question.question_text,
                    question_type=question_payload.question.question_type,
                )
                if question_payload.question
                else None
            )
            options_dto: List[DTOUpdateOptionInput] = [
                DTOUpdateOptionInput(
                    option_id=option_payload.option_id,
                    option_text=option_payload.option_text,
                    is_correct=option_payload.is_correct,
                )
                for option_payload in question_payload.options
            ]
            questions_dto.append(
                DTOUpdateQuestionInput(
                    question_id=question_id,
                    question=question_base_dto,
                    options=options_dto,
                )
            )
        try:
            return self.service.update_practice_test(
                user_id,
                practice_test_id,
                DTOUpdatePracticeTestInput(
                    base_info=base_info_dto, questions=questions_dto
                ),
            )
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_option(
        self, user_id: UUID, practice_test_id: UUID, payload: List[DeleteOptions]
    ) -> bool:
        try:
            return self.service.delete_option(
                user_id,
                practice_test_id,
                [
                    DTODeleteOptions(
                        question_id=raw.question_id, option_id=raw.option_id
                    )
                    for raw in payload
                ],
            )
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except OptionNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_question(
        self, user_id: UUID, practice_test_id: UUID, question_id: List[UUID]
    ) -> bool:
        try:
            return self.service.delete_question(user_id, practice_test_id, question_id)
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except QuestionNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_practice_test(self, user_id: UUID, practice_test_id: UUID) -> bool:
        try:
            return self.service.delete_practice_test(user_id, practice_test_id)
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
