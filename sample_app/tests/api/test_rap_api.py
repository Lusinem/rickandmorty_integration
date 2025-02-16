import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from sample_app.ram_api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rick & Morty API Integration is healthy"}


@pytest.mark.parametrize("entity", ["character", "location", "episode"])
def test_fetch_valid_entity(entity):
    with patch("sample_app.service.fetch_service.FetchService.fetch_and_store", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"message": f"{entity} stored successfully", "count": 10}
        response = client.get(f"/fetch/{entity}/")
        assert response.status_code == 200
        assert response.json()["message"].startswith(entity)


def test_fetch_invalid_entity():
    response = client.get("/fetch/invalid_entity/")
    assert response.status_code == 400
    assert "Invalid entity" in response.json()["detail"]
