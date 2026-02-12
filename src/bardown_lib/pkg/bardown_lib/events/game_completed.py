from datetime import datetime
from pydantic import UUID5, BaseModel
from typing import List, Optional

from pkg.bardown_lib.events.event_metadata import EventMetadata

class GamePlayerStatistics(BaseModel):
    player_id: UUID5
    statistics: str

class GameTeam(BaseModel):
    team_id: UUID5
    is_home: bool
    statistics: Optional[List[GamePlayerStatistics]] = []
    

class GameCompletedEvent(BaseModel):
    metadata: EventMetadata
    game_id: str
    title: str
    date: Optional[datetime] = None
    teams: List[GameTeam]

