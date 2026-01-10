from typing import List
from bardown_lib.models.dao.game import Game as GameDAO
from bardown_lib.models.dto.game import Game as GameDTO
from bardown_lib.models.dao.game_result import GameResult as GameResultDAO
from bardown_lib.models.dto.game_result import (
    GameResult as GameResultDTO,
    GameTeamResult,
    PlayerWithStatistics,
)
from bardown_lib.models.dto.statistics import Statistics


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


def game_result_DAO_to_game_result_DTO(game_dao: List[GameResultDAO]) -> GameResultDTO:
    result = GameResultDTO()
    home = GameTeamResult()
    away = GameTeamResult()
    result.home = home
    result.away = away

    result.game_id = game_dao[0].game_id
    result.title = game_dao[0].title
    result.date = game_dao[0].date
    result.score = game_dao[0].score
    result.location = game_dao[0].location
    home.team_id = game_dao[0].home_team_id
    home.roster = []
    away.team_id = game_dao[0].away_team_id
    away.roster = []

    for game in game_dao:
        player = PlayerWithStatistics(
            player_id=game.player_id,
            first_name=game.first_name,
            last_name=game.last_name,
            position=game.position,
            number=game.number,
            statistics=Statistics.from_string(game.statistics),
            img_url=game.player_image_url,
        )
        if game.team_id == home.team_id:
            home.roster.append(player)
            home.img_url = game.team_image_url
            home.name = game.team_name
        else:
            away.roster.append(player)
            away.img_url = game.team_image_url
            away.name = game.team_name

    return result
