import pytest

from src.logger import Logger
from src.player_data_service.players.models.dao.player import Player
from tests.bin.decorators.timed import timed
from tests.constants import VALID_PLAYER

logger = Logger("test")


@timed(logger)
def test_create_single_player_dao_instance() -> None:
    player = Player(**VALID_PLAYER)
    logger.debug(player)
    assert player is not None
