__version__ = "1.0.0"
__author__ = "Zac Foteff"

from bin.logger import Logger
from players.mappers.player_mapper import (
    player_DAO_to_player_DTO,
    player_DTO_to_player_DAO,
)
from players.models.dao.player import Player as PlayerDAO
from players.models.dto.player import Player as PlayerDTO
from tests.bin.decorators.timed import timed
from tests.constants import VALID_PLAYER

logger = Logger("test")


@timed(logger)
def test_valid_player_DAO_to_player_DTO() -> None:
    player_dao = PlayerDAO(**VALID_PLAYER)
    player_dto = player_DAO_to_player_DTO(player_dao=player_dao)
    assert player_dto is not None


@timed(logger)
def test_valid_player_DTO_to_player_DAO() -> None:
    player_dto = PlayerDTO(
        number=VALID_PLAYER["number"],
        first_name=VALID_PLAYER["first_name"],
        last_name=VALID_PLAYER["last_name"],
        position=VALID_PLAYER["position"],
        grade=VALID_PLAYER["grade"],
        school=VALID_PLAYER["school"],
    )
    player_dao = player_DTO_to_player_DAO(player_dto=player_dto)
    assert (
        player_dao is not None
        and player_dao.created is None
        and player_dao.modified is None
    )


@timed(logger)
def test_invalid_player_DTO_to_player_DAO() -> None:
    pass
