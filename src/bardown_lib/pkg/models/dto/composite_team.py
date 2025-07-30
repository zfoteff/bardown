from typing import List, Optional

from .player import Player
from pydantic import BaseModel


class Roster(BaseModel):
    year: Optional[int]
    players: Optional[List[Player]]


class CompositeTeam(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    img_url: Optional[str] = None
    roster: Optional[List[Roster]]
