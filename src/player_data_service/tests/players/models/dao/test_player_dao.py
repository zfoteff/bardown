__version__ = "1.0.0"
__author__ = "Zac Foteff"

from bin.logger import Logger
from players.models.dao.player import Player
from tests.bin.decorators.timed import timed
from tests.constants import VALID_PLAYER, VALID_PLAYER_TUPLE

logger = Logger("test")


@timed(logger)
def test_create_single_player_dao_instance() -> None:
    player = Player(**VALID_PLAYER)
    logger.debug(player)
    assert player is not None


@timed(logger)
def test_create_single_player_dao_instance_from_tuple() -> None:
    player = Player.from_tuple(VALID_PLAYER_TUPLE)
    logger.debug(player)
    assert player is not None
