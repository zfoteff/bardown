from re import I
from typing import Iterable, List

from models.coach import Coach
from models.composite_game_statistics import CompositeGameStatistics
from models.composite_season_statistics_full import (
    CompositeSeasonByYear,
    CompositeSeasonStatisticsFull,
)
from models.composite_statistics import CompositeStatistics
from models.composite_team import CompositeTeam, Roster
from models.game import Game
from models.game_result import GameResult, GameTeamResult, PlayerWithStatistics
from models.player import Player
from models.player_statistics import PlayerStatistics
from models.statistics import Statistics
from models.team import Team


def player_data_service_response_to_players(data: Iterable) -> List[Player]:
    return [Player(**player) for player in data]


def player_data_sevice_response_to_teams(data: Iterable) -> List[Team]:
    return [Team(**team) for team in data]


def player_data_service_response_to_games(data: Iterable) -> List[Game]:
    return [Game(**game) for game in data]


def player_data_service_response_to_game_result(data: Iterable) -> GameResult:
    return GameResult(
        game_id=data["game_id"],
        title=data["title"],
        date=data["date"],
        score=data["score"],
        location=data["location"],
        home=GameTeamResult(
            team_id=data["home"]["team_id"],
            name=data["home"]["name"],
            img_url=data["home"]["img_url"],
            roster=[
                PlayerWithStatistics(
                    player_id=player["player_id"],
                    first_name=player["first_name"],
                    last_name=player["last_name"],
                    position=player["position"],
                    number=player["number"],
                    statistics=Statistics(player["statistics"]),
                    img_url=player["img_url"],
                )
                for player in data["home"]["roster"]
            ],
        ),
        away=GameTeamResult(
            team_id=data["away"]["team_id"],
            name=data["away"]["name"],
            img_url=data["away"]["img_url"],
            roster=[
                PlayerWithStatistics(
                    player_id=player["player_id"],
                    first_name=player["first_name"],
                    last_name=player["last_name"],
                    position=player["position"],
                    number=player["number"],
                    statistics=Statistics(**player["statistics"]),
                    img_url=player["img_url"],
                )
                for player in data["away"]["roster"]
            ],
        ),
    )


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


def composite_teams_response_to_composite_teams(data: Iterable) -> List[CompositeTeam]:
    return [
        CompositeTeam(
            team_id=composite_team["team_id"],
            name=composite_team["name"],
            location=composite_team["location"],
            img_url=composite_team["img_url"],
            rosters=[
                Roster(
                    year=roster["year"],
                    players=[Player(**player) for player in roster["players"]],
                    coaches=[Coach(**coach) for coach in roster["coaches"]],
                )
                for roster in composite_team["rosters"]
            ],
        )
        for composite_team in data
    ]
