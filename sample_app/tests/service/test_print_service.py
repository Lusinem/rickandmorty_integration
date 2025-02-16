from unittest.mock import AsyncMock

import pytest

from sample_app.repositories.episode_repository import EpisodeRepository
from sample_app.service.print_service import PrintService


@pytest.mark.asyncio
async def test_print_filtered_episodes():
    mock_repository = AsyncMock(spec=EpisodeRepository)

    episode_1 = AsyncMock()
    episode_1.aired_in_range.return_value = True
    episode_1.RawData.name = "Episode 1"

    episode_2 = AsyncMock()
    episode_2.aired_in_range.return_value = True
    episode_2.RawData.name = "Episode 2"

    mock_repository.load_episodes.return_value = [episode_1, episode_2]

    service = PrintService(mock_repository)

    response = await service.print_filtered_episodes(2017, 2021)

    assert response["episodes"] == ["Episode 1", "Episode 2"]


@pytest.mark.asyncio
async def test_print_filtered_episodes_no_data():
    mock_repository = AsyncMock(spec=EpisodeRepository)
    mock_repository.load_episodes.return_value = []
    service = PrintService(mock_repository)

    response = await service.print_filtered_episodes(2017, 2021)

    assert "No episode data found" in response["message"]


@pytest.mark.asyncio
async def test_print_filtered_episodes_invalid_range():
    mock_repository = AsyncMock(spec=EpisodeRepository)
    service = PrintService(mock_repository)

    response = await service.print_filtered_episodes(2022, 2017)

    assert "Invalid date range" in response["error"]
