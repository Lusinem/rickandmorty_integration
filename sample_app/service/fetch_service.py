import logging
from sample_app.utils.json_writer import save_json
import logging

from sample_app.utils.json_writer import save_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FetchService:

    def __init__(self, api_client, entity: str):
        self.api_client = api_client
        self.entity = entity

    async def fetch_and_store(self):
        logger.info(f"Fetching data for entity: {self.entity}")

        try:
            data = await self.api_client.fetch_all(self.entity)
            if not data:
                logger.warning(f"No data found for {self.entity}")
                return {"message": f"No data found for {self.entity}"}

            await save_json(self.entity, data)

            logger.info(f"Stored {len(data)} {self.entity}s successfully.")
            return {"message": f"{self.entity} stored successfully", "count": len(data)}

        except Exception as e:
            logger.exception(f"Error fetching or storing {self.entity} data: {e}")
            return {"error": f"Failed to fetch and store {self.entity} data."}