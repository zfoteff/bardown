from models.player import Player
from typing import Self, List


class GameStatistics:
    _game_title: str
    _date: str
    _statistics: str

    def __init__(self, game_title: str, date: str, statistics: str) -> None:
        self._game_title = game_title
        self._date = date
        self._statistics = statistics

    @property
    def game_title(self) -> str:
        return self._game_title

    @property
    def date(self) -> str:
        return self._date

    @property
    def statistics(self) -> str:
        return self._statistics

    def to_dict(self) -> str:
        return {"game_title": self._game_title, "date": self._date, "statistics": self._statistics}


class CompositeStatistics:
    _season: str
    _games: List[GameStatistics]

    def __init__(self, season: str, games: GameStatistics) -> Self:
        self._season = season
        self._games = games

    @property
    def season(self) -> str:
        return self._season

    @property
    def games(self) -> List[GameStatistics]:
        return self._games

    def to_dict(self) -> dict:
        return {
            "season": f"{self._season}",
            "games": [game_stat.to_dict() for game_stat in self._games],
        }


class PlayerWithStatistics:
    _player: Player
    _statistics: CompositeStatistics

    def __init__(self, player: Player, statistics: CompositeStatistics) -> None:
        self._player = player
        self._statistics = statistics

    @property
    def player(self) -> Player:
        return self._player

    @property
    def statistics(self) -> CompositeStatistics:
        return self._statistics

    def to_dict(self) -> dict:
        return {"player": self._player.to_dict(), "statistics": self._statistics.to_dict()}
