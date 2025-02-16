from client.api.api_client import APIClient
from sample_app.repositories.episode_repository import EpisodeRepository

api_client = APIClient()


async def get_api_client():
    return api_client


def get_episode_repository():
    return EpisodeRepository()
