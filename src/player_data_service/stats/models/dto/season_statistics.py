from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from stats.models.statistics import Statistics


class SeasonStatistics(BaseModel):
    player_id: Optional[str] = None
    team_id: Optional[str] = None
    year: Optional[str] = None
    statistics: Optional[Statistics] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
