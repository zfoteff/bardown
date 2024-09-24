from models.player import Player
from typing import Self

class GameStatistics:
    _name: str
    _date: str

class CompositeStatistics:
    _season: str
    _games: GameStatistics

    def __init__(
        self,
        season: str,
        games: GameStatistics
    ) -> Self:

class PlayerWithStatistics:
    _player: Player
    _statistics: CompositeStatistics
