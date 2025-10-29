from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from wisho.controllers.search import SearchController
from wisho.core.db.session import get_async_session
from wisho.repositories.entry import EntryRepository
from wisho.schemas.entry import GetEntry

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[GetEntry])
async def search_entries(
    q: str = Query(..., min_length=1, description="Search query string"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
) -> list[GetEntry]:
    repository = EntryRepository(session)
    controller = SearchController(repository)

    return await controller.search(q, limit, offset)
