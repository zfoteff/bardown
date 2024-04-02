from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from src.player_data_service.players.models.enums.grade import Grade
from src.player_data_service.players.models.enums.position import Position


class Player(BaseModel):
    player_id: Optional[UUID] = uuid4()
    number: int
    first_name: str
    last_name: str
    position: Position
    grade: Grade
    school: str
