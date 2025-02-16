import pytest
from unittest.mock import AsyncMock, patch

from sample_app.service.fetch_service import FetchService


@pytest.mark.asyncio
async def test_fetch_and_store():
    mock_api_client = AsyncMock()
    mock_api_client.fetch_all.return_value = [{"id": 1, "name": "Character 1"}]

    with patch("sample_app.service.fetch_service.save_json", new_callable=AsyncMock) as mock_save_json:
        service = FetchService(mock_api_client, "character")
        response = await service.fetch_and_store()

        # Ensure save_json was awaited properly
        mock_save_json.assert_awaited()
        mock_save_json.assert_awaited_with("character", [{"id": 1, "name": "Character 1"}])

        assert response == {"message": "character stored successfully", "count": 1}

@pytest.mark.asyncio
async def test_fetch_and_store_no_data():
    mock_api_client = AsyncMock()
    mock_api_client.fetch_all.return_value = []
    service = FetchService(mock_api_client, "character")
    response = await service.fetch_and_store()
    assert "No data found" in response["message"]


@pytest.mark.asyncio
async def test_fetch_and_store_exception():
    mock_api_client = AsyncMock()
    mock_api_client.fetch_all.side_effect = Exception("API failure")
    service = FetchService(mock_api_client, "character")
    response = await service.fetch_and_store()
    assert "Failed to fetch and store character data" in response["error"]
