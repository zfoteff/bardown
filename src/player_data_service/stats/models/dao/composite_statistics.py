from typing import List, Self


class CompositeStatistics:
    games: List[CompositeGameStatistics]
    season: List[CompositeSeasonStatistics]

    def __init__(
        self,
        game_stats: List[CompositeGameStatistics],
        season_stats: List[CompositeSeasonStatistics],
    ) -> None:
        pass
