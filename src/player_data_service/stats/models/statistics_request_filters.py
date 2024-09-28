from typing import Optional

from pydantic import BaseModel


class GameStatisticsRequestFilters(BaseModel):
    player_id: Optional[str] = None
    game_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order: Optional[str] = None
    order_by: Optional[str] = None


class SeasonStatisticsRequestFilters(BaseModel):
    player_id: Optional[str] = None
    team_id: Optional[str] = None
    year: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order: Optional[str] = None
    order_by: Optional[str] = None
