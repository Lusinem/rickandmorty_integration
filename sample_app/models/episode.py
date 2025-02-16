from typing import Dict, Any, List, Union
from uuid import UUID

from pydantic import BaseModel


class EpisodeRawData(BaseModel):
    id: int
    name: str
    air_date: str
    episode: str
    characters: List[str]
    url: str
    created: str

    def aired_in_range(self, start_year: int, end_year: int) -> bool:
        try:
            year = int(self.air_date.split()[-1])
            return start_year <= year <= end_year
        except ValueError:
            return False


class Episode(BaseModel):
    id: UUID
    RawData: Union[EpisodeRawData, Dict[str, Any]]

    def aired_in_range(self, start_year: int, end_year: int) -> bool:
        if isinstance(self.RawData, dict):
            self.RawData = EpisodeRawData(**self.RawData)

        return self.RawData.aired_in_range(start_year, end_year)
