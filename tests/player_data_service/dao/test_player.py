import pytest

from src.logger import Logger
from src.player_data_service.players.dao.player import Player
from tests.constants import VALID_PLAYER_DAO
from tests.bin.decorators import timed

logger = Logger("player_dao_test")

@timed(logger)
def test_create_single_player_instance() -> None:
    player = Player(**VALID_PLAYER_DAO)
    logger.debug(player)
    assert player is not None
