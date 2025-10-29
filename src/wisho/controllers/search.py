from wisho.repositories.entry import EntryRepository
from wisho.schemas.entry import GetEntry


class SearchController:
    def __init__(self, repository: EntryRepository) -> None:
        self.repository = repository

    async def search(self, query: str, limit: int = 20, offset: int = 0) -> list[GetEntry]:
        entries = await self.repository.search(query=query, limit=limit, offset=offset)
        return [GetEntry.model_validate(entry) for entry in entries]
