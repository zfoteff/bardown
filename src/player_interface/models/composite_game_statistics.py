from typing import List, Self

from models.player_statistics import PlayerStatistics


class CompositeGameStatistics:
    _game_id: str
    _title: str
    _statistics: List[PlayerStatistics]

    def __init__(self, game_id: str, title: str, statistics: List[PlayerStatistics]) -> Self:
        self._game_id = game_id
        self._title = title
        self._statistics = statistics

    @property
    def game_id(self) -> str:
        return self._game_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def statistics(self) -> List[PlayerStatistics]:
        return self._statistics

    def to_dict(self) -> dict:
        return {
            "game_id": self._game_id,
            "title": self._title,
            "statistics": [player_stats.to_dict() for player_stats in self.statistics],
        }
