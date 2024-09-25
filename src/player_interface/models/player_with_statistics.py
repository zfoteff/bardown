from models.player import Player
from typing import Self


class GameStatistics:
    _name: str
    _date: str
    _statistics: str

    def __init__(self, name: str, date: str, statistics: str) -> None:
        self._name = name
        self._date = date
        self._statistics = statistics
        

class CompositeStatistics:
    _season: str
    _games: GameStatistics

    def __init__(self, season: str, games: GameStatistics) -> Self:
        self._season = season
        self._games = games

    @property
    def season(self) -> str:
        return self._season

    @property
    def games(self) -> GameStatistics:
        return self._games


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
