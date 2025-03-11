from typing import Optional

from pydantic import BaseModel


class Statistics(BaseModel):
    player_id: str
    statistics: str
