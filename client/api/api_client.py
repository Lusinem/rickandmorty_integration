import logging
from typing import List, Dict, Any, Optional

import httpx

from client.config import BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:

    def __init__(self):
        try:
            self.client = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0,
                                            headers={"User-Agent": "RickAndMortyClient/1.0"})
            logger.info("APIClient initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize API client: %s", e)
            raise

    async def fetch_one(self, entity: str, entity_id: int) -> Optional[Dict[str, Any]]:
        url = f"/{entity}/{entity_id}"
        logger.info(f"Fetching single entity: {url}")
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} while fetching {url}: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error while fetching {url}: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while fetching {url}: {e}")
        return None

    async def fetch_all(self, entity: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        results = []
        url = f"/{entity}"
        params = filters or {}

        logger.info(f"Fetching all entities: {url} with params {params}")

        try:
            while url:
                logger.info(f"Requesting URL: {url}")
                response = await self.client.get(url, params=params if "?" not in url else None)
                response.raise_for_status()
                data = response.json()

                logger.info(f"Received response: {data}")

                results.extend(data.get("results", []))

                next_url = data.get("info", {}).get("next")
                if not next_url:
                    logger.info("No more pages, stopping pagination.")
                    break

                url = next_url.replace(BASE_URL, "") if next_url.startswith(BASE_URL) else next_url
                params = None

                logger.info(f"Moving to next page: {url}")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} while fetching {url}: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error while fetching {url}: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while fetching {url}: {e}")

        return results

    async def close(self):
        """Close the async client session."""
        logger.info("Closing API client session.")
        try:
            await self.client.aclose()
        except Exception as e:
            logger.exception("Error while closing API client: %s", e)
