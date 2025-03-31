from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from stats.models.statistics import Statistics


class GameStatistics(BaseModel):
    player_id: Optional[str] = None
    game_id: Optional[str] = None
    statistics: Optional[Statistics] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
