from typing import Dict, List, Self


class PlayerSeasonStatistics:
    def __init__(self, player_id: str = None, statistics: str = None) -> Self:
        self.player_id = player_id
        self.statistics = statistics

    def to_dict(self) -> Dict:
        return {"player_id": f"{self.player_id}", "statistics": f"{self.statistics}"}


class CompositeSeasonStatistics:
    def __init__(self, year: int = None, players: List[PlayerSeasonStatistics] = None) -> Self:
        self.year = year
        self.players = players

    def to_dict(self) -> Dict:
        return {"year": self.year, "players": [player.to_dict for player in self.players]}
