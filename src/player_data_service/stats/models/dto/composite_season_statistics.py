from typing import List

from pydantic import BaseModel
from stats.models.statistics import Statistics


class PlayerSeasonStatistics(BaseModel):
    player_id: str = None
    statistics: Statistics = None


class CompositeSeasonStatistics(BaseModel):
    year: int = None
    players: List[PlayerSeasonStatistics] = None
