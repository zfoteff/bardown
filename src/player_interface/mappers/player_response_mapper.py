from typing import Iterable, List

from models.composite_game_statistics import CompositeGameStatistics
from models.composite_season_statistics_full import (
    CompositeSeasonByYear,
    CompositeSeasonStatisticsFull,
)
from models.composite_statistics import CompositeStatistics
from models.game import Game
from models.player import Player
from models.player_statistics import PlayerStatistics
from models.team import Team


def player_data_service_response_to_players(data: Iterable) -> List[Player]:
    return [Player(**player) for player in data]


def player_data_sevice_response_to_teams(data: Iterable) -> List[Team]:
    return [Team(**team) for team in data]


def player_data_service_response_to_games(data: Iterable) -> List[Game]:
    return [Game(**game) for game in data]


def composite_season_to_composite_season_by_year(
    seasons: List[CompositeSeasonStatisticsFull],
) -> List[CompositeSeasonByYear]:
    result = {}

    for season in seasons:
        if season["year"] not in result.keys():
            result[season["year"]] = [season]
        else:
            result[season["year"]].append(season)

    return [
        CompositeSeasonByYear(
            year,
            [
                CompositeSeasonStatisticsFull(**year_composite_stats)
                for year_composite_stats in result[year]
            ],
        )
        for year in result.keys()
    ]


def player_data_service_response_to_composite_statistics(
    data: Iterable, order_by_year: bool = False
) -> CompositeStatistics:
    return CompositeStatistics(
        games=[
            CompositeGameStatistics(
                game_id=game["game_id"],
                title=game["title"],
                statistics=[
                    PlayerStatistics(
                        player_id=player_stats["player_id"],
                        statistics=player_stats["statistics"],
                    )
                    for player_stats in game["statistics"]
                ],
            )
            for game in data["games"]
        ],
        season=(
            [
                CompositeSeasonStatisticsFull(
                    year=season["year"],
                    team_id=season["team_id"],
                    team_name=season["team_name"],
                    players=[
                        PlayerStatistics(
                            player_id=season_stats["player_id"],
                            statistics=season_stats["statistics"],
                        )
                        for season_stats in season["players"]
                    ],
                )
                for season in data["season"]
            ]
            if not order_by_year
            else composite_season_to_composite_season_by_year(data["season"])
        ),
    )
