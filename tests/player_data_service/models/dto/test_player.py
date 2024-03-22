import pytest

from src.logger import Logger
from src.player_data_service.players.models.dto.player import Player
from tests.bin.decorators.timed import timed
from tests.constants import VALID_PLAYER_DAO

logger = Logger("test")


@timed(logger)
def test_create_single_player_instance() -> None:
    player = Player(**VALID_PLAYER_DAO)
    logger.debug(player)
    assert player is not None
