from games.models.dao.game import Game as GameDAO
from games.models.dto.game import Game as GameDTO
from games.models.dao.game_result import GameResult as GameResultDAO
from games.models.dto.game_result import GameResult as GameResultDTO


def game_DTO_to_game_DAO(game_dto: GameDTO) -> GameDAO:
    return GameDAO(dict(game_dto))


def game_DAO_to_game_DTO(game_dao: GameDAO) -> GameDTO:
    return GameDTO(
        game_id=game_dao.game_id,
        title=game_dao.title,
        date=game_dao.date,
        score=game_dao.score,
        location=game_dao.location,
        created=str(game_dao.created),
        modified=str(game_dao.modified),
    )


def game_result_DAO_to_game_result_DTO(game_dao: GameResultDAO) -> GameResultDTO:
    return GameResultDTO()
