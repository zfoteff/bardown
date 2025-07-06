from players.models.dao.coach import Coach as CoachDAO
from players.models.dto.coach import Coach as CoachDTO


def coach_DTO_to_coach_DAO(coach_dto: CoachDTO) -> CoachDAO:
    return CoachDAO(dict(coach_dto))


def coach_DAO_to_coach_DTO(coach_dao: CoachDAO) -> CoachDTO:
    return CoachDTO(
        coach_id=coach_dao.coach_id,
        first_name=coach_dao.first_name,
        last_name=coach_dao.last_name,
        since=coach_dao.since,
        email=coach_dao.email,
        phone_number=coach_dao.phone_number,
        imgurl=coach_dao.imgurl,
        created=coach_dao.created,
        modified=coach_dao.modified,
    )
