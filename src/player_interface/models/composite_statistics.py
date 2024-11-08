from typing import List, Self

from models.composite_game_statistics import CompositeGameStatistics
from models.composite_season_statistics import CompositeSeasonStatistics


class CompositeStatistics:
    _games: List[CompositeGameStatistics]
    _season: List[CompositeSeasonStatistics]

    def __init__(
        self, games: List[CompositeGameStatistics], season: List[CompositeSeasonStatistics]
    ) -> Self:
        self._games = games
        self._season = season

    @property
    def games(self) -> List[CompositeGameStatistics]:
        return self._games

    @property
    def season(self) -> List[CompositeSeasonStatistics]:
        return self._season

    def to_dict(self) -> dict:
        return {"games": self._games.to_dict(), "season": self._season.to_dict()}
