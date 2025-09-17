from players.models.dto.coach import Coach
from players.models.dto.player import Player
from teams.models.dao.team import Team as TeamDAO
from teams.models.dto.composite_team import CompositeTeam as CompositeTeamDTO, Roster
from teams.models.dao.composite_team import CompositeTeam as CompositeTeamDAO
from teams.models.dto.team import Team as TeamDTO


def team_DTO_to_team_DAO(team_dto: TeamDTO) -> TeamDAO:
    return TeamDAO(dict(team_dto))


def team_DAO_to_team_DTO(team_dao: TeamDAO) -> TeamDTO:
    return TeamDTO(
        team_id=team_dao.team_id,
        name=team_dao.name,
        location=team_dao.location,
        img_url=team_dao.imgurl,
        created=team_dao.created,
        modified=team_dao.modified,
    )


def composite_team_DAO_to_composite_team_DTO(composite_team_dao: CompositeTeamDAO):
    return CompositeTeamDTO(
        team_id=composite_team_dao.team.team_id,
        name=composite_team_dao.team.name,
        location=composite_team_dao.team.location,
        img_url=composite_team_dao.team.imgurl,
        roster=Roster(
            players=[
                Player(
                    player_id=player.player_id,
                    first_name=player.first_name,
                    last_name=player.last_name,
                    position=player.position,
                    number=player.number,
                    grade=player.grade,
                    school=player.school,
                    imgurl=player.img_url,
                )
                for player in composite_team_dao.players
            ],
            coaches=[
                Coach(
                    coach_id=coach.coach_id,
                    first_name=coach.first_name,
                    last_name=coach.last_name,
                    role=coach.role,
                    since=coach.since,
                    email=coach.email,
                    phone_number=coach.phone_number,
                    imgurl=coach.img_url,
                )
                for coach in composite_team_dao.coaches
            ],
        ),
    )
