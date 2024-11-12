__version__ = "1.0.0"
__author__ = "Zac Foteff"

from stats.models.dto.game_statistics import GameStatistics
from tests.bin.decorators.timed import timed
from tests.constants import VALID_GAME_STATISTICS

from bin.logger import Logger

logger = Logger("test")


@timed(logger)
def test_create_single_statistics_dto_instance() -> None:
    statistics = GameStatistics(**VALID_GAME_STATISTICS)
    logger.debug(statistics)
    assert statistics is not None
