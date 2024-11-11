from typing import List, Self

from models.player_statistics import PlayerStatistics


class CompositeSeasonStatistics:
    _year: int
    _team_id: str
    _players: List[PlayerStatistics]

    def __init__(self, year: int, team_id: str, players: List[PlayerStatistics]) -> Self:
        self._year = year
        self._team_id = team_id
        self._players = players

    @property
    def year(self) -> int:
        return self._year

    @property
    def team_id(self) -> str:
        return self._team_id

    @property
    def players(self) -> List[PlayerStatistics]:
        return self._players

    def to_dict(self) -> dict:
        return {
            "year": self._year,
            "team_id": self._team_id,
            "players": [player_stats.to_dict() for player_stats in self.players],
        }
