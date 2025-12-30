from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from players.models.enums.position import Position
from stats.models.statistics import Statistics


class PlayerWithStatistics(BaseModel):
    player_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[Position] = None
    number: Optional[Position] = None
    statistics: Optional[Statistics] = None
    img_url: Optional[str] = None


class GameTeamResult(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    img_url: Optional[str] = None
    roster: Optional[List[PlayerWithStatistics]] = list()


class GameResult(BaseModel):
    game_id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[datetime] = None
    score: Optional[str] = None
    location: Optional[str] = None
    home: Optional[GameTeamResult] = GameTeamResult()
    away: Optional[GameTeamResult] = GameTeamResult()
