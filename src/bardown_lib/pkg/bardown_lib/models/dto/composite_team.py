from typing import List, Optional

from .player import Player
from .coach import Coach
from pydantic import BaseModel


class Roster(BaseModel):
    year: Optional[int] = None
    players: Optional[List[Player]] = []
    coaches: Optional[List[Coach]] = []


class CompositeTeam(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    img_url: Optional[str] = "static/blank.jpg"
    roster: Optional[List[Roster]] = []
