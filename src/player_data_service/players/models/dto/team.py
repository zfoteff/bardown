from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Team(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
