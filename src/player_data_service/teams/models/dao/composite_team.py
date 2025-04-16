from typing import Dict, List, Self


class Roster:
    pass


class CompositeTeam:
    team_id: str
    name: str
    location: str
    img_url: str
    roster: List[Roster]

    def __init__(
        self, team_id: str, name: str, location: str, img_url: str, roster: List[Roster]
    ) -> Self:
        self.team_id = team_id
        self.name = name
        self.location = location
        self.img_url = img_url
        self.roster = roster

    def to_dict(self) -> Dict:
        return {"team_id": ""}
