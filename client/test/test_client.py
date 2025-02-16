import httpx
import pytest
import respx

from client.api.api_client import APIClient
from client.config import BASE_URL


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.asyncio
@respx.mock
async def test_fetch_one_success(api_client):

    character_id = 1
    expected_response = {"id": 1, "name": "Rick Sanchez"}

    # Mock the API response
    route = respx.get(f"{BASE_URL}/character/{character_id}").mock(
        return_value=httpx.Response(200, json=expected_response))

    result = await api_client.fetch_one("character", character_id)

    assert result == expected_response
    assert route.called, "API endpoint was not called"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_one_not_found(api_client):
    character_id = 9999

    respx.get(f"{BASE_URL}/character/{character_id}").mock(return_value=httpx.Response(404))

    result = await api_client.fetch_one("character", character_id)

    assert result is None, "Expected None for a 404 response"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_network_error(api_client):
    respx.get(f"{BASE_URL}/character").mock(side_effect=httpx.RequestError("Network Error"))

    result = await api_client.fetch_all("character")

    assert result == [], "Expected an empty list when a network error occurs"


@pytest.mark.asyncio
async def test_close(api_client):
    await api_client.close()
    assert api_client.client.is_closed, "Client session was not closed"
