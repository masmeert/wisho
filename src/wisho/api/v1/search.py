from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from wisho.controllers.search import SearchController
from wisho.core.db.session import get_async_session
from wisho.repositories.word import WordRepository

router = APIRouter(prefix="/search", tags=["search"])


class GetSearchResults(BaseModel):
    id: int = Field(..., description="Internal word ID")
    headwords: list[str] = Field(default_factory=list, description="Kanji forms of the word")
    readings: list[str] = Field(default_factory=list, description="Kana readings")
    glosses: list[str] = Field(default_factory=list, description="English (or translated) glosses")
    score: float = Field(..., description="Computed search relevance score")


@router.get("", response_model=list[GetSearchResults])
async def search_entries(
    q: str = Query(..., min_length=1, description="Search query string"),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
) -> list[GetSearchResults]:
    repository = WordRepository(session)
    controller = SearchController(repository)

    return await controller.search(q, limit)
