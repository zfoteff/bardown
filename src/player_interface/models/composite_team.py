from typing import List, Optional
from pydantic import BaseModel

from models.coach import Coach
from models.player import Player


class Roster(BaseModel):
    year: Optional[int] = None
    players: Optional[List[Player]] = []
    coaches: Optional[List[Coach]] = []


class CompositeTeam(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    img_url: Optional[str] = None
    rosters: Optional[List[Roster]] = []
