from datetime import datetime
from typing import Self

from .enums.grade import Grade
from .enums.position import Position


class Player:
    _player_id: str
    _number: int
    _first_name: str
    _last_name: str
    _position: Position
    _grade: Grade
    _school: str
    _img_url: str
    _created: datetime
    _modified: datetime

    def __init__(
        self,
        player_id: str,
        number: int,
        first_name: str,
        last_name: str,
        position: str,
        grade: str,
        school: str,
        imgurl: str,
        created: str,
        modified: str,
    ) -> Self:
        self._player_id = player_id
        self._number = number
        self._first_name = first_name
        self._last_name = last_name
        self._position = Position(position)
        self._grade = Grade(grade)
        self._school = school
        self._img_url = imgurl
        self._created = datetime.fromisoformat(created)
        self._modified = datetime.fromisoformat(modified)

    @property
    def player_id(self) -> str:
        return self._player_id

    @property
    def number(self) -> int:
        return self._number

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @property
    def position(self) -> str:
        return str(self._position)

    @property
    def grade(self) -> str:
        return str(self._grade)

    @property
    def school(self) -> str:
        return self._school

    @property
    def img_url(self) -> str:
        return self._img_url

    @property
    def created(self) -> str:
        return str(self._created)

    @property
    def modified(self) -> str:
        return str(self._modified)

    def to_dict(self, full_definition: bool = False) -> dict:
        player_dict = {
            "player_id": self._player_id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "position": self._position,
            "grade": self._grade,
            "school": self._school,
            "img_url": self._img_url,
        }

        if full_definition:
            player_dict.update({"created": self._created, "modified": self._modified})

        return player_dict
