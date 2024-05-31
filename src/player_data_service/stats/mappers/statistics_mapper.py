from stats.models.dao.game_statistics import GameStatistics as GameStatisticsDAO
from stats.models.dto.game_statistics import GameStatistics as GameStatisticsDTO
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


def game_statistics_DAO_to_game_statistics_DTO(
    game_stats_dao: GameStatisticsDAO,
) -> GameStatisticsDTO:
    statistics = Statistics()
    statistics.statistics_from_string(game_stats_dao.statistics)

    return GameStatisticsDTO(
        player_id=game_stats_dao.player_id,
        game_id=game_stats_dao.game_id,
        statistics=statistics,
        created=game_stats_dao.created,
        modified=game_stats_dao.modified,
    )
