from fastapi import status, HTTPException

from app.application.services.search_service import SearchServices
from app.presentation.schemas.search_schema import SearchInput, SearchOutput


class SearchController:
    def __init__(self, service: SearchServices):
        self.service = service

    def search_by_keyword(self, query_input: SearchInput):
        try:
            result = self.service.search_by_keyword(query_input)
            return SearchOutput(
                courses=result.get("courses"),
                practice_tests=result.get("practice_tests"),
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Đã xảy ra lỗi không mong muốn.",
            )
