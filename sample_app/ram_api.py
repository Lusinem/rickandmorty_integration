import logging

from fastapi import FastAPI, Depends, Query, HTTPException

from sample_app.dependencies import get_api_client, get_episode_repository
from sample_app.service.fetch_service import FetchService
from sample_app.service.print_service import PrintService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

ALLOWED_ENTITIES = {"character", "location", "episode"}


@app.get("/")
async def health_check():
    return {"message": "Rick & Morty API Integration is healthy"}


@app.get("/fetch/{entity}/")
async def fetch_data(
        entity: str,
        api_client=Depends(get_api_client)
):
    if entity not in ALLOWED_ENTITIES:
        logger.warning(f"Invalid entity requested: {entity}")
        raise HTTPException(status_code=400, detail=f"Invalid entity '{entity}'. Allowed: {ALLOWED_ENTITIES}")

    service = FetchService(api_client, entity)

    try:
        data = await service.fetch_and_store()
        return data
    except Exception as e:
        logger.exception(f"Error fetching data for entity {entity}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/filter-episodes/")
async def get_filtered_episodes(
        start_year: int = Query(2017, description="Filter from year"),
        end_year: int = Query(2021, description="Filter up to year"),
        repository=Depends(get_episode_repository),
):
    service = PrintService(repository)
    return await service.print_filtered_episodes(start_year, end_year)
