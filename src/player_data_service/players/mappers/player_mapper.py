from players.models.dao.player import Player as PlayerDAO
from players.models.dto.player import Player as PlayerDTO
from players.models.enums.grade import Grade
from players.models.enums.position import Position


def player_DTO_to_player_DAO(player_dto: PlayerDTO) -> PlayerDAO:
    return PlayerDAO(dict(player_dto))


def player_DAO_to_player_DTO(player_dao: PlayerDAO) -> PlayerDTO:
    return PlayerDTO(
        player_id=player_dao.player_id,
        number=player_dao.number,
        first_name=player_dao.first_name,
        last_name=player_dao.last_name,
        position=Position(player_dao.position),
        grade=Grade(player_dao.grade),
        school=player_dao.school,
        created=player_dao.created,
        modified=player_dao.modified,
    )
