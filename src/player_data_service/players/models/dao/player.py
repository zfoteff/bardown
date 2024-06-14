from datetime import datetime
from typing import Dict, Self, Tuple

from players.models.enums.grade import Grade
from players.models.enums.position import Position


class Player:
    def __init__(
        self,
        player_id: str = None,
        number: int = None,
        first_name: str = None,
        last_name: str = None,
        position: Position = None,
        grade: Grade = None,
        school: str = None,
        imgurl: str = None,
        created: datetime = None,
        modified: datetime = None,
    ) -> Self:
        self.player_id = player_id
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.grade = grade
        self.school = school
        self.imgurl = imgurl
        self.created = created
        self.modified = modified

    @classmethod
    def from_tuple(cls, player_tuple: Tuple) -> None:
        """Create player from a tuple

        Args:
            player_tuple (Tuple): Tuple containing ordered player data
        """
        return cls(**{k: v for k, v in zip(cls().to_dict().keys(), player_tuple)})

    def __str__(self) -> str:
        return (
            f"{self.number}. {self.last_name}, {self.first_name} [{self.position}] "
            + "| {self.grade} at {self.school}"
        )

    def to_dict(self) -> Dict:
        return {
            "player_id": f"{self.player_id}",
            "number": self.number,
            "first_name": f"{self.first_name}",
            "last_name": f"{self.last_name}",
            "position": self.position,
            "grade": self.grade,
            "school": f"{self.school}",
            "imgurl": f"{self.imgurl}",
            "created": f"{self.created}",
            "modified": f"{self.modified}",
        }
