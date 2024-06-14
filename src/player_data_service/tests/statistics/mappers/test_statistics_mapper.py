from datetime import datetime

from bin.logger import Logger
from stats.mappers.statistics_mapper import (
    game_statistics_DAO_to_game_statistics_DTO,
    game_statistics_DTO_to_game_statistics_DAO,
)
from stats.models.dao.game_statistics import GameStatistics as GameStatisticsDAO
from stats.models.dto.game_statistics import GameStatistics as GameStatisticsDTO
from stats.models.statistics import Statistics
from tests.bin.decorators.timed import timed
from tests.constants import (
    VALID_GAME_STATISTICS,
    VALID_GAME_STATISTICS_STRING,
    VALID_UUID_0,
    VALID_UUID_1,
)

logger = Logger("test")


@timed(logger)
def test_valid_game_statistics_DAO_to_game_statistics_DTO() -> None:
    game_stats_dao = GameStatisticsDAO(
        player_id=VALID_UUID_0,
        game_id=VALID_UUID_1,
        statistics=VALID_GAME_STATISTICS_STRING,
        created=datetime.now(),
        modified=datetime.now(),
    )
    game_stats_dto = game_statistics_DAO_to_game_statistics_DTO(game_stats_dao=game_stats_dao)
    assert game_stats_dto is not None


@timed(logger)
def test_valid_game_statistics_DTO_to_game_statistics_DAO() -> None:
    game_stats_dto = GameStatisticsDTO(
        player_id=VALID_UUID_0,
        game_id=VALID_UUID_1,
        statistics=Statistics(**VALID_GAME_STATISTICS),
        created=datetime.now(),
        modified=datetime.now(),
    )
    game_stats_dao = game_statistics_DTO_to_game_statistics_DAO(game_stats_dto)
    assert game_stats_dao is not None
