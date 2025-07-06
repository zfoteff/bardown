from typing import Optional

from pydantic import BaseModel


class Team(BaseModel):
    team_id: Optional[str]
    is_home: bool
    statistics: Optional[List[Statistics]]
