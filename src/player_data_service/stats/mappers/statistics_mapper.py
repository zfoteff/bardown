import statistics
from re import S

from stats.models.dao.composite_game_statistics import (
    CompositeGameStatistics as CompositeGameStatistics,
)
from stats.models.dao.composite_season_statistics import (
    CompositeSeasonStatistics as CompositeSeasonStatisticsDAO,
)
from stats.models.dao.composite_statistics import (
    CompositeStatistics as CompositeStatisticsDAO,
)
from stats.models.dao.game_statistics import GameStatistics as GameStatisticsDAO
from stats.models.dao.season_statistics import SeasonStatistics as SeasonStatisticsDAO
from stats.models.dto.composite_game_statistics import (
    CompositeGameStatistics as CompositeGameStatisticsDTO,
)
from stats.models.dto.composite_game_statistics import (
    PlayerGameStatistics as PlayerGameStatisticsDTO,
)
from stats.models.dto.composite_season_statistics import (
    CompositeSeasonStatistics as CompositeSeasonStatisticsDTO,
)
from stats.models.dto.composite_season_statistics import (
    PlayerSeasonStatistics as PlayerSeasonStatisticsDTO,
)
from stats.models.dto.composite_statistics import (
    CompositeStatistics as CompositeStatisticsDTO,
)
from stats.models.dto.game_statistics import GameStatistics as GameStatisticsDTO
from stats.models.dto.season_statistics import SeasonStatistics as SeasonStatisticsDTO
from stats.models.statistics import Statistics


def game_statistics_DTO_to_game_statistics_DAO(
    game_stats_dto: GameStatisticsDTO,
) -> GameStatisticsDAO:
    return GameStatisticsDAO(
        player_id=game_stats_dto.player_id,
        game_id=game_stats_dto.game_id,
        statistics=str(game_stats_dto.statistics),
        created=game_stats_dto.created,
        modified=game_stats_dto.modified,
    )


def season_statistics_DTO_to_season_statistics_DAO(
    season_stats_dto: SeasonStatisticsDTO,
) -> SeasonStatisticsDAO:
    return SeasonStatisticsDAO(
        player_id=season_stats_dto.player_id,
        team_id=season_stats_dto.team_id,
        year=season_stats_dto.year,
        statistics=str(season_stats_dto.statistics),
        created=season_stats_dto.created,
        modified=season_stats_dto.modified,
    )


def game_statistics_DAO_to_game_statistics_DTO(
    game_stats_dao: GameStatisticsDAO,
) -> GameStatisticsDTO:
    statistics = Statistics.from_string(game_stats_dao.statistics)

    return GameStatisticsDTO(
        player_id=game_stats_dao.player_id,
        game_id=game_stats_dao.game_id,
        statistics=statistics,
        created=game_stats_dao.created,
        modified=game_stats_dao.modified,
    )


def season_statistics_DAO_to_season_statistics_DTO(
    season_stats_dao: SeasonStatisticsDAO,
) -> SeasonStatisticsDTO:
    statistics = Statistics.from_string(season_stats_dao.statistics)

    return SeasonStatisticsDTO(
        player_id=season_stats_dao.player_id,
        team_id=season_stats_dao.team_id,
        year=season_stats_dao.year,
        statistics=statistics,
        created=season_stats_dao.created,
        modified=season_stats_dao.modified,
    )


def composite_player_game_statistics_DAO_to_DTO() -> PlayerGameStatisticsDTO:
    pass


def composite_player_season_statistics_DAO_to_DTO(
    player_season_statistics_dao: PlayerSeasonStatisticsDAO,
) -> PlayerSeasonStatisticsDTO:
    statistics = Statistics.from_string(player_season_statistics_dao.statistics)

    return PlayerSeasonStatisticsDTO(
        player_id=player_season_statistics_dao.player_id, statistics=statistics
    )


def composite_statistics_DTO_to_composite_statistics_DAO(
    composite_stats_dto: CompositeStatisticsDTO,
) -> CompositeStatisticsDAO:
    pass


def composite_statistics_DAO_to_composite_statistics_DTO(
    composite_stats_dao: CompositeStatisticsDAO,
) -> CompositeStatisticsDTO:
    game_data = {}

    for game in composite_stats_dao.games:
        if game.game_id not in game_data.keys():
            game_data[game.game_id] = [{"player_id": game.player_id, "statistics": game.statistics}]
        else:
            game_data[game.game_id].append(
                {"player_id": game.player_id, "statistics": game.statistics}
            )

    game_stats = [
        CompositeGameStatisticsDTO(
            game_id,
            [
                PlayerGameStatisticsDTO(
                    player_id=player_game_info.get("player_id"),
                    statistics=Statistics.from_string(player_game_info.get("statistics")),
                )
                for player_game_info in game_data[game_id]
            ],
        )
        for game_id in game_data.keys()
    ]

    season_data = {}

    for season in composite_stats_dao.season:
        if (season.year, season.team_id) not in game_data.keys():
            season_data[(season.year, season.team_id)] = [{""}]

    season_stats = [
        CompositeSeasonStatisticsDTO(
            season.year,
            [
                composite_player_season_statistics_DAO_to_DTO(player_season_statistics)
                for player_season_statistics in season.players
            ],
        )
        for season in composite_stats_dao.season
    ]

    return CompositeStatisticsDTO(game=game_stats, season=season_stats)
