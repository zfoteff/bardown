from typing import List, Optional

from players.models.dto.coach import Coach
from players.models.dto.player import Player
from pydantic import BaseModel


class Roster(BaseModel):
    year: Optional[int]
    players: Optional[List[Player]]
    coaches: Optional[List[Coach]]


class CompositeTeam(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    img_url: Optional[str] = None
    roster: Optional[List[Roster]]
