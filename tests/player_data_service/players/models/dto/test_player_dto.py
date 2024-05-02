__version__ = "1.0.0"
__author__ = "Zac Foteff"

from bin.logger import Logger

from src.player_data_service.players.models.dto.player import Player
from tests.bin.constants import VALID_PLAYER
from tests.bin.decorators.timed import timed

logger = Logger("test")


@timed(logger)
def test_create_single_player_dto_instance() -> None:
    player = Player(
        number=VALID_PLAYER["number"],
        first_name=VALID_PLAYER["first_name"],
        last_name=VALID_PLAYER["last_name"],
        position=VALID_PLAYER["position"],
        grade=VALID_PLAYER["grade"],
        school=VALID_PLAYER["school"],
    )
    logger.debug(player)
    assert player is not None


@timed(logger)
def test_create_single_player_dto_instance_with_optional_fields() -> None:
    player = Player(
        number=VALID_PLAYER["number"],
        first_name=VALID_PLAYER["first_name"],
        last_name=VALID_PLAYER["last_name"],
        position=VALID_PLAYER["position"],
        grade=VALID_PLAYER["grade"],
        school=VALID_PLAYER["school"],
        created=VALID_PLAYER["created"],
        modified=VALID_PLAYER["modified"],
    )
    logger.debug(player)
    assert player is not None
