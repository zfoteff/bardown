from typing import List, Optional

from pydantic import BaseModel
from players.models.dto.player import PlayerWithNumber


class Roster(BaseModel):
    year: Optional[int]
    players: Optional[List[PlayerWithNumber]]


class CompositeTeam(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    img_url: Optional[str] = None
    roster: Optional[List[Roster]]
