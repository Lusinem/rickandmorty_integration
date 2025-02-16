import logging

from sample_app.repositories.episode_repository import EpisodeRepository

logger = logging.getLogger(__name__)


class PrintService:

    def __init__(self, repository: EpisodeRepository):
        self.repository = repository

    async def print_filtered_episodes(self, start_year: int, end_year: int):
        try:
            if start_year > end_year:
                logger.error(f"Invalid date range: start_year={start_year} cannot be greater than end_year={end_year}")
                return {"error": "Invalid date range: start_year cannot be greater than end_year"}

            episodes = self.repository.load_episodes()

            if not episodes:
                logger.warning("No episode data found in repository.")
                return {"message": "No episode data found."}

            filtered_episodes = [
                ep.RawData.name for ep in episodes if ep.aired_in_range(start_year, end_year)
            ]

            if not filtered_episodes:
                logger.info(f"No episodes found between {start_year} and {end_year}.")
                return {"message": f"No episodes found between {start_year} and {end_year}"}

            logger.info(f"Episodes between {start_year}-{end_year}: {filtered_episodes}")
            return {"episodes": filtered_episodes}

        except Exception as e:
            logger.exception(f"Unexpected error while filtering episodes: {e}")
            return {"error": "An unexpected error occurred while processing episodes."}
