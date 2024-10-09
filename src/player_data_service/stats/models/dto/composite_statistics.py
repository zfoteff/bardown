from typing import Optional, List

from pydantic import BaseModel

from stats.models.dto.composite_game_statistics import CompositeGameStatistics
from stats.models.dto.composite_season_statistics import CompositeSeasonStatistics


class CompositeStatistics(BaseModel):
    games: Optional[List[CompositeGameStatistics]] = None
    season: Optional[List[CompositeSeasonStatistics]] = None
