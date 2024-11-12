from games.models.dao.game import Game
from tests.bin.decorators.timed import timed
from tests.constants import VALID_GAME, VALID_GAME_TUPLE

from bin.logger import Logger

logger = Logger("test")


@timed(logger)
def test_create_single_game_dao_instance() -> None:
    game = Game(**VALID_GAME)
    logger.debug(game)
    assert game is not None


@timed(logger)
def test_create_single_game_dao_instance_from_tuple() -> None:
    game = Game.from_tuple(VALID_GAME_TUPLE)
    logger.debug(game)
    assert game is not None
