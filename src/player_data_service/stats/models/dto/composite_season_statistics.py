from pydantic import BaseModel

from stats.models.dto.composite_game_statistics import PlayerGameStatistics


class CompositeSeasonStatistics(BaseModel):
    year: int = None
    players: PlayerGameStatistics = None
