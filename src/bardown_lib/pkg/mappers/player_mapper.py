from models.dao.player import Player as PlayerDAO
from models.dto.player import Player as PlayerDTO
from enums import grade, position


def player_DTO_to_player_DAO(player_dto: PlayerDTO) -> PlayerDAO:
    return PlayerDAO(dict(player_dto))


def player_DAO_to_player_DTO(player_dao: PlayerDAO) -> PlayerDTO:
    return PlayerDTO(
        player_id=player_dao.player_id,
        first_name=player_dao.first_name,
        last_name=player_dao.last_name,
        position=position.Position(player_dao.position),
        grade=grade.Grade(player_dao.grade),
        school=player_dao.school,
        imgurl=player_dao.imgurl,
        created=player_dao.created,
        modified=player_dao.modified,
    )
