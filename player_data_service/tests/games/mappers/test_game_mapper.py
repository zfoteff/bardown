from games.mappers.game_mapper import game_DAO_to_game_DTO, game_DTO_to_game_DAO
from games.models.dao.game import Game as GameDAO
from games.models.dto.game import Game as GameDTO
from tests.bin.decorators.timed import timed
from tests.constants import VALID_GAME

from bin.logger import Logger

logger = Logger("test")


@timed(logger)
def test_valid_game_DAO_to_game_DTO() -> None:
    game_dao = GameDAO(**VALID_GAME)
    game_dto = game_DAO_to_game_DTO(game_dao=game_dao)
    assert game_dto is not None


@timed(logger)
def test_valid_game_DTO_to_game_DAO() -> None:
    game_dto = GameDTO(
        game_id=VALID_GAME["game_id"],
        title=VALID_GAME["title"],
        date=VALID_GAME["date"],
        score=VALID_GAME["score"],
        location=VALID_GAME["location"],
        created=VALID_GAME["created"],
        modified=VALID_GAME["modified"],
    )
    game_dao = game_DTO_to_game_DAO(game_dto)
    assert game_dao is not None
