from bin.logger import Logger
from games.mappers.game_mapper import (
    game_DAO_to_game_DTO,
    game_DTO_to_game_DAO,
)
from games.models.dao.game import Game as GameDAO
from games.models.dto.game import Game as GameDTO
from tests.bin.decorators.timed import timed
from tests.constants import VALID_GAME

logger = Logger("test")


@timed(logger)
def test_valid_game_DAO_to_game_DTO() -> None:
    game_dao = GameDAO(**VALID_GAME)
    game_dto = game_DAO_to_game_DTO(game_dao=game_dao)
    assert game_dto is not None


@timed(logger)
def test_valid_game_DTO_to_game_DAO() -> None:
    game_dto = GameDTO()
