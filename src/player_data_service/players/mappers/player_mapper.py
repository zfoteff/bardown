from bardown_lib.models.dao.player import Player as PlayerDAO
from bardown_lib.models.dto.player import Player as PlayerDTO
from bardown_lib.enums.grade import Grade
from bardown_lib.enums.position import Position


def player_DTO_to_player_DAO(player_dto: PlayerDTO) -> PlayerDAO:
    return PlayerDAO(dict(player_dto))


def player_DAO_to_player_DTO(player_dao: PlayerDAO) -> PlayerDTO:
    return PlayerDTO(
        player_id=player_dao.player_id,
        first_name=player_dao.first_name,
        last_name=player_dao.last_name,
        position=Position(player_dao.position),
        number=player_dao.number,
        grade=Grade(player_dao.grade),
        school=player_dao.school,
        imgurl=player_dao.imgurl,
        created=player_dao.created,
        modified=player_dao.modified,
    )
