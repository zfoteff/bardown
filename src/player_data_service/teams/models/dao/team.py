from datetime import datetime
from typing import Dict, Self, Tuple


class Team:
    def __init__(
        self,
        team_id: str = None,
        name: str = None,
        created: datetime = None,
        modified: datetime = None,
    ) -> Self:
        self.team_id = team_id
        self.name = name
        self.created = created
        self.modified = modified

    @classmethod
    def from_tuple(cls, team_tuple: Tuple) -> None:
        """Create team from a tuple

        Args:
            player_tuple (Tuple): Tuple containing ordered team data
        """
        return cls(**{k: v for k, v in zip(cls().to_dict().keys(), team_tuple)})

    def __str__(self) -> str:
        return f"{self.name}"

    def to_dict(self) -> Dict:
        return {
            "team_id": f"{self.team_id}",
            "name": f"{self.name}",
            "date": f"{self.date}",
            "score": f"{self.score}",
            "location": f"{self.location}",
            "created": f"{self.created}",
            "modified": f"{self.modified}",
        }
