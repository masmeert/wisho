from unittest.mock import AsyncMock

import pytest

from wisho.controllers.search import SearchController
from wisho.models.entry import Entry
from wisho.repositories.entry import EntryRepository
from wisho.schemas.entry import GetEntry


class TestSearchController:
    """Test suite for SearchController."""

    @pytest.fixture
    def mock_repository(self) -> AsyncMock:
        """Create a mock EntryRepository."""
        return AsyncMock(spec=EntryRepository)

    @pytest.fixture
    def controller(self, mock_repository: AsyncMock) -> SearchController:
        """Create a SearchController instance with mocked repository."""
        return SearchController(repository=mock_repository)

    @pytest.mark.asyncio
    async def test_search_returns_results(
        self, controller: SearchController, mock_repository: AsyncMock, sample_entry: Entry
    ) -> None:
        """Test search returns properly formatted results."""
        mock_repository.search.return_value = [sample_entry]

        results = await controller.search(query="school")

        assert len(results) == 1
        assert isinstance(results[0], GetEntry)
        assert results[0].id == 1206730
        assert results[0].kanji_forms[0].text == "学校"
        mock_repository.search.assert_called_once_with(query="school", limit=20, offset=0)

    @pytest.mark.asyncio
    async def test_search_returns_multiple_results(
        self, controller: SearchController, mock_repository: AsyncMock, sample_multiple_entries: list[Entry]
    ) -> None:
        """Test search returns multiple results."""
        mock_repository.search.return_value = sample_multiple_entries

        results = await controller.search(query="test")

        assert len(results) == 2
        assert results[0].id == 1206730
        assert results[1].id == 1000300
        mock_repository.search.assert_called_once_with(query="test", limit=20, offset=0)

    @pytest.mark.asyncio
    async def test_search_returns_empty_list(self, controller: SearchController, mock_repository: AsyncMock) -> None:
        """Test search returns empty list when no entries found."""
        mock_repository.search.return_value = []

        results = await controller.search(query="nonexistent")

        assert results == []
        mock_repository.search.assert_called_once_with(query="nonexistent", limit=20, offset=0)
