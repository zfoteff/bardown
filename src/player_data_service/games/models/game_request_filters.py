from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class GameRequestFilters(BaseModel):
    game_id: Optional[str] = None
    date: Optional[datetime] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order: Optional[str] = None
    order_by: Optional[str] = None
