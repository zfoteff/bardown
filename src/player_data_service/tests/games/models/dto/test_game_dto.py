from bin.logger import Logger
from games.models.dto.game import Game
from tests.bin.decorators.timed import timed
from tests.constants import VALID_GAME

logger = Logger("test")


@timed(logger)
def test_create_single_game_dto_instance() -> None:
    game = Game(
        game_id=VALID_GAME["game_id"],
        title=VALID_GAME["title"],
        date=VALID_GAME["date"],
        score=VALID_GAME["score"],
        location=VALID_GAME["location"],
        created=VALID_GAME["created"],
        modified=VALID_GAME["modified"],
    )
    logger.debug(game)
    assert game is not None
