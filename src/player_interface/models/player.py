from datetime import datetime
from typing import Self, Optional

from pydantic import BaseModel

from .enums.grade import Grade
from .enums.position import Position


class Player(BaseModel):
    player_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    position: Optional[Position]
    number: Optional[int]
    grade: Optional[Grade]
    school: Optional[str]
    imgurl: Optional[str]
    created: Optional[datetime]
    modified: Optional[datetime]

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self, full_definition: bool = False) -> dict:
        player_dict = {
            "player_id": self.player_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "position": self.position,
            "number": self.number,
            "grade": self.grade,
            "school": self.school,
            "img_url": self.imgurl,
        }

        if full_definition:
            player_dict.update({"created": self.created, "modified": self.modified})

        return player_dict
