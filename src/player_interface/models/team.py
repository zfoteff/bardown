from datetime import datetime
from typing import Self


class Team:
    _team_id: str
    _name: str
    _location: str
    _img_url: str
    _created: datetime
    _modified: datetime

    def __init__(
        self,
        team_id: str,
        name: str,
        location: str,
        imgurl: str,
        created: str,
        modified: str
    ) -> Self:
        self._team_id = team_id
        self._name = name
        self._location = location
        self._img_url = imgurl
        self._created = datetime.fromisoformat(created)
        self._modified = datetime.fromisoformat(modified)

    @property
    def team_id(self) -> str:
        return self._team_id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def location(self) -> str:
        return self._location
    
    @property
    def img_url(self) -> str:
        return self._img_url

    @property
    def created(self) -> str:
        return str(self._created)

    @property
    def modified(self) -> str:
        return str(self._modified)
