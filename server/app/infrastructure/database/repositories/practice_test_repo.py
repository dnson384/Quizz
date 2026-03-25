from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy import func, tuple_, asc
from typing import List, Optional
from uuid import UUID
from dataclasses import dataclass

from app.domain.entities.practice_test.practice_test_entity import (
    PracticeTest,
    PracticeTestOutput,
    NewBaseInfoInput,
    UpdateBaseInfoInput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    PracticeTestQuestion,
    QuestionOutput,
    NewQuestionBaseInput,
    UpdateQuestionBaseInput,
    QuestionWithOptionsOutput,
)
from app.domain.entities.practice_test.answer_option_entity import (
    AnswerOption,
    AnswerOptionOutput,
    NewAnswerOptionInput,
    UpdateAnswerOptionInput,
    DeleteOption,
)
from app.domain.exceptions.practice_test_exception import (
    PracticeTestsNotFoundErrorDomain,
    ResultNotFoundErrorDomain,
    UserNotAllowThisResultErrorDomain,
)
from app.domain.entities.practice_test.practice_test_results_entity import (
    PracticeTestResult,
    ResultInput,
    ResultOutput,
    ResultWithHistory,
    ResultWithPracticeTest,
)
from app.domain.entities.practice_test.practice_test_histories import (
    PracticeTestHistory,
    HistoryInput,
    HistoryOutput,
    QuestionHistory,
)


from app.infrastructure.database.models.practice_test_model import (
    PracticeTestModel,
    PracticeTestQuestionModel,
    AnswerOptionModel,
    PracticeTestResultModel,
    PracticeTestHistoryModel,
)
from app.infrastructure.database.models.user_model import UserModel
from app.infrastructure.mappers import Mapper

from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)


@dataclass(frozen=True)
class QuestionDetailOutput:
    question: QuestionOutput
    options: List[AnswerOptionOutput]


@dataclass(frozen=True)
class PraceticeTestWithDetailsResponse:
    base_info: PracticeTestOutput
    questions: List[QuestionDetailOutput]


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
    options: List[UpdateAnswerOptionInput]


class PracticeTestRepository(IPracticeTestRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_practice_tests_by_user_id(self, user_id: UUID) -> List[PracticeTestOutput]:
        practice_tests = (
            self.db.query(
                PracticeTestModel.practice_test_id,
                PracticeTestModel.practice_test_name,
                UserModel.avatar_url,
                UserModel.username,
            )
            .join(UserModel, PracticeTestModel.practice_test_user)
            .filter(PracticeTestModel.user_id == user_id)
            .all()
        )
        if not practice_tests:
            raise PracticeTestsNotFoundErrorDomain("Người dùng không có bài kiểm tra")
        return [
            PracticeTestOutput(
                practice_test_id=practice_test.practice_test_id,
                practice_test_name=practice_test.practice_test_name,
                author_avatar_url=practice_test.avatar_url,
                author_username=practice_test.username,
            )
            for practice_test in practice_tests
        ]

    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestOutput]:
        try:
            query = (
                self.db.query(
                    PracticeTestModel.practice_test_id,
                    PracticeTestModel.practice_test_name,
                    UserModel.avatar_url,
                    UserModel.username,
                )
                .filter(PracticeTestModel.practice_test_name.ilike(f"%{keyword}%"))
                .join(UserModel, PracticeTestModel.user_id == UserModel.user_id)
            )

            if cursor_id:
                query = query.filter(PracticeTestModel.practice_test_id < cursor_id)

            query = query.order_by(PracticeTestModel.practice_test_id)

            db_results = query.limit(12).all()

            domain_results: List[PracticeTestOutput] = []
            for row in db_results:
                domain_results.append(
                    PracticeTestOutput(
                        practice_test_id=row.practice_test_id,
                        practice_test_name=row.practice_test_name,
                        author_avatar_url=row.avatar_url,
                        author_username=row.username,
                    )
                )
            return domain_results

        except Exception as e:
            print("Error occurred when query practice test", e)
            return []

    def get_random_practice_test(self) -> List[PracticeTestOutput]:
        try:
            query = (
                self.db.query(
                    PracticeTestModel.practice_test_id,
                    PracticeTestModel.practice_test_name,
                    UserModel.username.label("author_username"),
                    UserModel.avatar_url.label("author_avatar_url"),
                )
                .join(UserModel, UserModel.user_id == PracticeTestModel.user_id)
                .order_by(func.random())
                .limit(3)
                .all()
            )

            domain_result: List[PracticeTestOutput] = []
            for item in query:
                domain_result.append(
                    PracticeTestOutput(
                        practice_test_id=item.practice_test_id,
                        practice_test_name=item.practice_test_name,
                        author_avatar_url=item.author_avatar_url,
                        author_username=item.author_username,
                    )
                )

            return domain_result

        except Exception as e:
            print("Có lỗi xảy ra khi lấy bài kiểm tra thử ngẫu nhiên", e)
            return []

    def check_user_practice_test(self, user_id: UUID, practice_test_id: UUID):
        if (
            not self.db.query(PracticeTestModel)
            .filter(PracticeTestModel.practice_test_id == practice_test_id)
            .first()
        ):
            raise PracticeTestsNotFoundErrorDomain("Không tìm thấy bài kiểm tra thử")
        return (
            self.db.query(PracticeTestModel)
            .join(UserModel, PracticeTestModel.practice_test_user)
            .filter(UserModel.user_id == user_id)
            .filter(PracticeTestModel.practice_test_id == practice_test_id)
            .first()
        )

    def get_practice_test_detail_by_id(
        self, practice_test_id: str
    ) -> PraceticeTestWithDetailsResponse:
        test_query = (
            self.db.query(
                PracticeTestModel.practice_test_id,
                PracticeTestModel.practice_test_name,
                UserModel.username.label("author_username"),
                UserModel.avatar_url.label("author_avatar_url"),
            )
            .filter(PracticeTestModel.practice_test_id == practice_test_id)
            .join(UserModel, UserModel.user_id == PracticeTestModel.user_id)
        ).first()

        if not test_query:
            raise PracticeTestsNotFoundErrorDomain(
                f"Không tồn tại bài kiểm tra {practice_test_id}"
            )

        base_info_domain = PracticeTestOutput(
            practice_test_id=test_query.practice_test_id,
            practice_test_name=test_query.practice_test_name,
            author_avatar_url=test_query.author_avatar_url,
            author_username=test_query.author_username,
        )

        questions_id_query = (
            self.db.query(PracticeTestQuestionModel.question_id)
            .filter(PracticeTestQuestionModel.practice_test_id == practice_test_id)
            .order_by(asc(PracticeTestQuestionModel.question_id))
            .all()
        )

        questions_ids = [qid[0] for qid in questions_id_query]

        question_query = (
            self.db.query(PracticeTestQuestionModel)
            .filter(PracticeTestQuestionModel.question_id.in_(questions_ids))
            .options(selectinload(PracticeTestQuestionModel.question_anwser_opt))
            .all()
        )

        questions_map = {q.question_id: q for q in question_query}

        questions_domain: List[QuestionDetailOutput] = []
        for question_id in questions_ids:
            if question_id in questions_map:
                question = questions_map[question_id]
                questions_domain.append(
                    QuestionDetailOutput(
                        question=QuestionOutput(
                            question_id=question.question_id,
                            question_text=question.question_text,
                            question_type=question.question_type,
                        ),
                        options=[
                            AnswerOptionOutput(
                                option_id=option.option_id,
                                option_text=option.option_text,
                                is_correct=option.is_correct,
                            )
                            for option in question.question_anwser_opt
                        ],
                    )
                )

        return PraceticeTestWithDetailsResponse(
            base_info=base_info_domain, questions=questions_domain
        )

    def get_practice_test_random_detail_by_id(
        self, practice_test_id: str, count: int
    ) -> PraceticeTestWithDetailsResponse:
        test_query = (
            self.db.query(
                PracticeTestModel.practice_test_id,
                PracticeTestModel.practice_test_name,
                UserModel.username.label("author_username"),
                UserModel.avatar_url.label("author_avatar_url"),
            )
            .filter(PracticeTestModel.practice_test_id == practice_test_id)
            .join(UserModel, UserModel.user_id == PracticeTestModel.user_id)
        ).first()

        if not test_query:
            raise PracticeTestsNotFoundErrorDomain(
                f"Không tồn tại bài kiểm tra {practice_test_id}"
            )

        base_info_domain = PracticeTestOutput(
            practice_test_id=test_query.practice_test_id,
            practice_test_name=test_query.practice_test_name,
            author_avatar_url=test_query.author_avatar_url,
            author_username=test_query.author_username,
        )

        questions_id_query = (
            self.db.query(PracticeTestQuestionModel.question_id)
            .filter(PracticeTestQuestionModel.practice_test_id == practice_test_id)
            .order_by(func.random())
            .limit(count)
            .all()
        )

        questions_ids = [qid[0] for qid in questions_id_query]

        question_query = (
            self.db.query(PracticeTestQuestionModel)
            .filter(PracticeTestQuestionModel.question_id.in_(questions_ids))
            .options(selectinload(PracticeTestQuestionModel.question_anwser_opt))
            .all()
        )

        questions_map = {q.question_id: q for q in question_query}

        questions_domain: List[QuestionDetailOutput] = []
        for question_id in questions_ids:
            if question_id in questions_map:
                question = questions_map[question_id]
                questions_domain.append(
                    QuestionDetailOutput(
                        question=QuestionOutput(
                            question_id=question.question_id,
                            question_text=question.question_text,
                            question_type=question.question_type,
                        ),
                        options=[
                            AnswerOptionOutput(
                                option_id=option.option_id,
                                option_text=option.option_text,
                                is_correct=option.is_correct,
                            )
                            for option in question.question_anwser_opt
                        ],
                    )
                )

        return PraceticeTestWithDetailsResponse(
            base_info=base_info_domain, questions=questions_domain
        )

    def get_all_histories(self, user_id: UUID):
        result_query = (
            self.db.query(PracticeTestResultModel)
            .filter(PracticeTestResultModel.user_id == user_id)
            .options(
                selectinload(PracticeTestResultModel.result_practice_test)
                .load_only(
                    PracticeTestModel.practice_test_id,
                    PracticeTestModel.practice_test_name,
                )
                .selectinload(PracticeTestModel.practice_test_user)
                .load_only(
                    UserModel.avatar_url,
                    UserModel.username,
                )
            )
            .all()
        )

        result_with_test_domain: List[ResultWithPracticeTest] = []
        for result in result_query:
            result_domain = ResultOutput(
                result_id=result.result_id,
                num_of_questions=result.num_of_questions,
                score=result.score,
            )

            practice_result = result.result_practice_test
            user_result = practice_result.practice_test_user
            practice_test_domain = PracticeTestOutput(
                practice_test_id=practice_result.practice_test_id,
                practice_test_name=practice_result.practice_test_name,
                author_avatar_url=user_result.avatar_url,
                author_username=user_result.username,
            )

            result_with_test_domain.append(
                ResultWithPracticeTest(
                    result=result_domain, base_info=practice_test_domain
                )
            )
        return result_with_test_domain

    def get_practice_test_history(
        self, user_id: UUID, result_id: UUID, practice_test_id: UUID
    ):
        result_query = (
            self.db.query(PracticeTestResultModel)
            .filter(PracticeTestResultModel.result_id == result_id)
            .first()
        )
        if not result_query:
            raise ResultNotFoundErrorDomain
        elif (
            result_query.user_id != user_id
            or result_query.practice_test_id != practice_test_id
        ):
            raise UserNotAllowThisResultErrorDomain

        practice_test_query = (
            self.db.query(
                PracticeTestModel.practice_test_id,
                PracticeTestModel.practice_test_name,
                UserModel.username.label("author_username"),
                UserModel.avatar_url.label("author_avatar_url"),
            )
            .filter(PracticeTestModel.practice_test_id == result_query.practice_test_id)
            .join(UserModel, UserModel.user_id == PracticeTestModel.user_id)
            .first()
        )
        if not practice_test_query:
            raise PracticeTestsNotFoundErrorDomain

        history_query = (
            self.db.query(PracticeTestHistoryModel)
            .filter(PracticeTestHistoryModel.result_id == result_query.result_id)
            .options(
                selectinload(PracticeTestHistoryModel.history_question)
                .load_only(
                    PracticeTestQuestionModel.question_text,
                    PracticeTestQuestionModel.question_type,
                )
                .selectinload(PracticeTestQuestionModel.question_anwser_opt)
                .load_only(AnswerOptionModel.option_text, AnswerOptionModel.is_correct)
            )
            .all()
        )

        result_domain = ResultOutput(
            result_id=result_query.result_id,
            num_of_questions=result_query.num_of_questions,
            score=result_query.score,
        )
        practice_test_domain = PracticeTestOutput(
            practice_test_id=practice_test_query.practice_test_id,
            practice_test_name=practice_test_query.practice_test_name,
            author_avatar_url=practice_test_query.author_avatar_url,
            author_username=practice_test_query.author_username,
        )

        history_domain: List[QuestionHistory] = []
        for history in history_query:
            existing_question = next(
                (
                    item
                    for item in history_domain
                    if item.question_id == history.question_id
                ),
                None,
            )

            if existing_question:
                existing_question.history.option_id.append(history.option_id)
                continue

            options_domain = [
                AnswerOptionOutput(
                    option_id=opt.option_id,
                    option_text=opt.option_text,
                    is_correct=opt.is_correct,
                )
                for opt in history.history_question.question_anwser_opt
            ]

            question_domain = QuestionWithOptionsOutput(
                question_id=history.history_question.question_id,
                question_text=history.history_question.question_text,
                question_type=history.history_question.question_type,
                options=options_domain,
            )

            history_item = HistoryOutput(
                history_id=history.history_id,
                option_id=[history.option_id],
                question_detail=question_domain,
            )

            history_domain.append(
                QuestionHistory(question_id=history.question_id, history=history_item)
            )

        return ResultWithHistory(
            result=result_domain,
            base_info=practice_test_domain,
            histories=history_domain,
        )

    def create_new_practice_test(self, payload: NewPracticeTestInput):
        try:
            # Thêm thông tin cơ bản
            new_practice_test_domain: PracticeTest = Mapper.new_practice_test_domain(
                payload.base_info
            )
            new_practice_test_model: PracticeTestModel = (
                Mapper.practice_test_domain_to_model(new_practice_test_domain)
            )
            self.db.add(new_practice_test_model)

            # Thêm câu hỏi
            new_questions_model: List[PracticeTestQuestionModel] = []
            for question_payload in payload.questions:
                new_question_domain: PracticeTestQuestion = Mapper.new_question_domain(
                    new_practice_test_domain.practice_test_id, question_payload.question
                )
                new_question_model: PracticeTestQuestionModel = (
                    Mapper.question_domain_to_model(new_question_domain)
                )

                for option_payload in question_payload.options:
                    new_option_domail: AnswerOption = Mapper.new_option_domain(
                        new_question_domain.question_id, option_payload
                    )
                    new_question_model.question_anwser_opt.append(
                        Mapper.option_domain_to_model(new_option_domail)
                    )

                new_questions_model.append(new_question_model)
            self.db.add_all(new_questions_model)
            self.db.commit()
            return True
        except Exception as e:
            print("Lỗi khi thêm bài kiểm tra thử mới", e)
            self.db.rollback()
            raise e

    def submit_test(
        self, user_id: UUID, result: ResultInput, histories: List[HistoryInput]
    ) -> UUID:
        new_result: PracticeTestResult = Mapper.new_result_domain(user_id, result)
        new_histories: List[PracticeTestHistory] = [
            Mapper.new_history_domain(new_result.result_id, history)
            for history in histories
        ]

        result_model: PracticeTestResultModel = (
            Mapper.practice_test_result_domain_to_model(new_result)
        )
        histories_model: List[PracticeTestHistoryModel] = (
            Mapper.practice_test_history_domain_to_model(history_domain)
            for history_domain in new_histories
        )

        try:
            self.db.add(result_model)
            self.db.add_all(histories_model)
            self.db.commit()
            self.db.refresh(result_model)
            return result_model.result_id
        except Exception as e:
            self.db.rollback()
            raise e

    def update_practice_test(
        self,
        practice_test_id: UUID,
        base_info: Optional[UpdateBaseInfoInput],
        question_create: List[UpdateQuestionInput],
        question_update: List[UpdateQuestionInput],
    ):
        try:
            # Cập nhật thông tin cơ bản bài test (nếu có)
            if base_info:
                self.db.query(PracticeTestModel).filter(
                    PracticeTestModel.practice_test_id == practice_test_id
                ).update(
                    {PracticeTestModel.practice_test_name: base_info.practice_test_name}
                )

            # Thêm mới câu hỏi
            if question_create:
                questions_model: List[PracticeTestQuestionModel] = []
                for question in question_create:
                    new_question_domain: PracticeTestQuestion = (
                        Mapper.new_question_domain(
                            practice_test_id, question.question_base
                        )
                    )
                    new_question_model: PracticeTestQuestionModel = (
                        Mapper.question_domain_to_model(new_question_domain)
                    )
                    for option in question.options:
                        new_option_model = Mapper.option_domain_to_model(
                            Mapper.new_option_domain(
                                new_question_domain.question_id,
                                NewAnswerOptionInput(
                                    option_text=option.option_text,
                                    is_correct=option.is_correct,
                                ),
                            )
                        )
                        new_question_model.question_anwser_opt.append(new_option_model)
                        questions_model.append(new_question_model)
                self.db.add_all(questions_model)

            # Cập nhật câu hỏi
            if question_update:
                question_ids = [question.question_id for question in question_update]
                questions = (
                    self.db.query(PracticeTestQuestionModel)
                    .filter(PracticeTestQuestionModel.question_id.in_(question_ids))
                    .options(
                        selectinload(PracticeTestQuestionModel.question_anwser_opt)
                    )
                    .all()
                )

                questions_map = {
                    question.question_id: question for question in questions
                }

                for question in question_update:
                    cur_question = questions_map[question.question_id]
                    # Cập nhật thông tin câu hỏi
                    if question.question_base:
                        cur_question.question_text = (
                            question.question_base.question_text
                        )
                        cur_question.question_type = (
                            question.question_base.question_type
                        )

                    # Cập nhật thông tin câu trả lời
                    for option in question.options:
                        # Thêm câu trả lời
                        if not option.option_id:
                            option_model = Mapper.option_domain_to_model(
                                Mapper.new_option_domain(
                                    question.question_id,
                                    NewAnswerOptionInput(
                                        option_text=option.option_text,
                                        is_correct=option.is_correct,
                                    ),
                                )
                            )

                            cur_question.question_anwser_opt.append(option_model)

                        # Cập nhật câu trả lời
                        else:
                            cur_option = next(
                                (
                                    o
                                    for o in cur_question.question_anwser_opt
                                    if o.option_id == option.option_id
                                ),
                                None,
                            )
                            if not cur_option:
                                raise ValueError(
                                    f"Không tồn tại câu trả lời {option.option_id} trong câu hỏi {cur_question.question_id}"
                                )
                            cur_option.option_text = option.option_text
                            cur_option.is_correct = option.is_correct
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_answer_option(
        self, practice_test_id: UUID, payload: List[DeleteOption]
    ) -> bool:
        pairs_to_delete = [(item.option_id, item.question_id) for item in payload]

        valid_questions_subquery = self.db.query(
            PracticeTestQuestionModel.question_id
        ).filter(PracticeTestQuestionModel.practice_test_id == practice_test_id)

        (
            self.db.query(AnswerOptionModel)
            .filter(
                tuple_(AnswerOptionModel.option_id, AnswerOptionModel.question_id).in_(
                    pairs_to_delete
                )
            )
            .filter(AnswerOptionModel.question_id.in_(valid_questions_subquery))
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return True

    def delete_question(self, practice_test_id: UUID, question_id: List[UUID]) -> bool:
        (
            self.db.query(PracticeTestQuestionModel)
            .filter(PracticeTestQuestionModel.question_id.in_(question_id))
            .filter(PracticeTestQuestionModel.practice_test_id == practice_test_id)
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return True

    def delete_practice_test(self, practice_test_id: UUID) -> bool:
        practice_test = (
            self.db.query(PracticeTestModel)
            .filter(PracticeTestModel.practice_test_id == practice_test_id)
            .first()
        )

        self.db.delete(practice_test)
        self.db.commit()
        return True
