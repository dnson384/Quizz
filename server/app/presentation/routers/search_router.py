from fastapi import APIRouter, Depends, status

from app.presentation.controllers.search_controller import SearchController
from app.presentation.dependencies.dependencies import get_search_controller
from app.presentation.schemas.search_schema import SearchInput, SearchOutput

router = APIRouter(prefix="/search", tags=["SEARCH"])


@router.get("/", response_model=SearchOutput, status_code=status.HTTP_200_OK)
def search_by_keyword(
    query_input: SearchInput = Depends(),
    controller: SearchController = Depends(get_search_controller),
):
    return controller.search_by_keyword(query_input=query_input)
