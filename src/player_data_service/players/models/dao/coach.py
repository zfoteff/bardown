from datetime import datetime
from typing import Self, Tuple


class Coach:
    def __init__(
        self,
        coach_id: str = None,
        first_name: str = None,
        last_name: str = None,
        role: str = None,
        phone_number: str = None,
        email: str = None,
        created: datetime = None,
        modified: datetime = None,
    ) -> Self:
        self.coach_id = coach_id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.phone_number = number
        self.email = email
        self.created = created
        self.modified = modified

    @classmethod
    def from_tuple(cls, coach_tuple: Tuple) -> None:
        """Create coach from a tuple

        Args:
            player_tuple (Tuple): Tuple containing ordered coach data
        """
        return cls(**{k: v for k, v in zip(cls().to_dict().keys(), coach_tuple)})

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name} [{self.role}] | phone: {self.phone_number}, email: {self.email}"

    def to_dict(self) -> str:
        return {
            "coach_id": f"{self.coach_id}",
            "first_name": f"{self.first_name}",
            "last_name": f"{self.last_name}",
            "role": f"{self.role}",
            "phone_number": f"{self.phone_number}",
            "email": f"{self.email}",
            "created": f"{self.created}",
            "modified": f"{self.modified}",
        }
