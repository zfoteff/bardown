from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Player(BaseModel):
    player_id: Optional[str] = None
    number: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    grade: Optional[str] = None
    school: Optional[str] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
