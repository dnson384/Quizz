from app.application.abstractions.course_abstraction import ICourseRepository
from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.domain.entities.course.course_entity import CourseInput


class SearchServices:
    def __init__(
        self,
        course_repo: ICourseRepository,
        practice_test_repo: IPracticeTestRepository,
    ):
        self.course_repo = course_repo
        self.practice_test_repo = practice_test_repo

    def search_by_keyword(self, query_input: CourseInput) -> dict:
        try:
            keyword = query_input.keyword
            type = query_input.type
            cursor_id = query_input.cursor_id
            courses_result = []
            practice_tests_result = []

            match type:
                case "all":
                    courses_result = self.course_repo.get_courses_by_keyword(keyword)

                    practice_tests_result = (
                        self.practice_test_repo.get_practice_tests_by_keyword(keyword)
                    )
                case "courses":
                    courses_result = self.course_repo.get_courses_by_keyword(
                        keyword, cursor_id
                    )
                case "practice_tests":
                    practice_tests_result = (
                        self.practice_test_repo.get_practice_tests_by_keyword(
                            keyword, cursor_id
                        )
                    )

            return {
                "courses": courses_result,
                "practice_tests": practice_tests_result,
            }
        except Exception as e:
            print("Lỗi trong quá trình tìm kiếm", e)
            raise
