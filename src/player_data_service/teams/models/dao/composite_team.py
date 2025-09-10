from teams.models.dao.team import Team
from typing import List


class CompositeTeamPlayer:
    team_id: str
    year: int
    player_id: str
    first_name: str
    last_name: str
    number: int
    position: str
    grade: str
    school: str
    img_url: str


class CompositeTeamCoach:
    team_id: str
    year: int
    coach_id: str
    first_name: str
    last_name: str
    role: str
    since: int
    img_url: str

    def __init__(
        self, team_id: str = None, year: int = None, coach_id: str = None, first_name: str = None
    ):
        pass


class CompositeTeam:
    team: Team
    players: List[CompositeTeamPlayer]
    coaches: List[CompositeTeamCoach]
