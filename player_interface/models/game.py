from datetime import datetime


class Game:
    _game_id: str
    _title: str
    _date: str
    _score: str
    _location: str
    _created: datetime
    _modified: datetime

    def __init__(
        self,
        game_id: str,
        title: str,
        date: datetime,
        score: str,
        location: str,
        created: datetime,
        modified: datetime,
    ) -> None:
        self._game_id = game_id
        self._title = title
        self._date = date
        self._score = score
        self._location = location
        self._created = created
        self._modified = modified

    @property
    def game_id(self) -> str:
        return self._game_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def date(self) -> str:
        date = datetime.fromisoformat(self._date)
        return f"{date.month}/{date.day} - {date.hour % 12}:{date.minute}"

    @property
    def score(self) -> str:
        return self._score

    @property
    def location(self) -> str:
        return self._location

    @property
    def created(self) -> str:
        return str(self._created)

    @property
    def modified(self) -> str:
        return str(self._modified)
