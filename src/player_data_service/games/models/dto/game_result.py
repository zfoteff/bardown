from typing import Optional
from pydantic import BaseModel


class GameTeamRoster(BaseModel):
    pass


class GameTeamResult(BaseModel):
    team_id: str
    roster: GameTeamRoster


class GameResult(BaseModel):
    game_id: str
    home: Optional[GameTeamResult]
    away: Optional[GameTeamResult]
