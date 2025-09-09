from typing import Dict, List, Self


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
    img_url: str
    coach_id: str
    first_name: str
    last_name: str
    role: str
    since: int
    img_url: str