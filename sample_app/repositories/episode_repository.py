import json
import logging
from pathlib import Path
from typing import List

from sample_app.models.episode import Episode

logger = logging.getLogger(__name__)


class EpisodeRepository:

    def __init__(self, file_path: str = "data/episode.json"):
        self.file_path = Path(file_path)

    def load_episodes(self) -> List[Episode]:
        if not self.file_path.exists():
            logger.warning("Episode data file not found.")
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Episode(**ep) for ep in data]
        except Exception as e:
            logger.exception(f"Error loading episodes from {self.file_path}: {e}")
            return []

