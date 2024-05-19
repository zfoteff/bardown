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
    def position(self) -> str:
        return str(self._position)

    @property
    def grade(self) -> str:
        return str(self._grade)

    @property
    def school(self) -> str:
        return self._school

    @property
    def created(self) -> str:
        return str(self._created)

    @property
    def modified(self) -> str:
        return str(self._modified)
