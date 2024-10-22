from typing import Dict, Self, Tuple


class PlayerGameStatistics:
    def __init__(self, player_id: str = None, statistics: str = None) -> Self:
        self.player_id = player_id
        self.statistics = statistics

    def to_dict(self) -> Dict:
        return {"player_id": f"{self.player_id}", "statistics": f"{self.statistics}"}


class CompositeGameStatistics:
    def __init__(self, game_id: str = None, statistics: PlayerGameStatistics = None) -> Self:
        self.game_id = game_id
        self.statistics = statistics

    @classmethod
    def from_tuple(cls, composite_statistics_tuple: Tuple) -> None:
        return cls(**{k: v for k, v in zip(cls().to_dict().keys(), composite_statistics_tuple)})

    def to_dict(self) -> Dict:
        return {
            "game_id": f"{self.game_id}",
            "statistics": [statistics.to_dict() for statistics in self.statistics],
        }
