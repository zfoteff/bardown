from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from models.enums.position import Position
from models.statistics import Statistics


class PlayerWithStatistics(BaseModel):
    player_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[Position] = None
    number: Optional[int] = 0
    statistics: Optional[Statistics] = None
    img_url: Optional[str] = "static/blank.jpg"

    @property
    def player_id(self) -> str:
        return self.player_id

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def position(self) -> str:
        return self.position

    @property
    def number(self) -> str:
        return self.number

    @property
    def statistics(self) -> Statistics:
        return self.statistics

    @property
    def img_url(self) -> str:
        return self.img_url


class GameTeamResult(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = "Team"
    img_url: Optional[str] = "static/blank.jpg"
    roster: Optional[List[PlayerWithStatistics]] = list()

    @property
    def name(self) -> str:
        return self.name

    @property
    def team_id(self) -> str:
        return self.team_id

    @property
    def img_url(self) -> str:
        return self.img_url

    @property
    def roster(self) -> str:
        return self.roster


class GameResult(BaseModel):
    game_id: Optional[str] = None
    title: Optional[str] = "Away @ Home"
    date: Optional[datetime] = None
    score: Optional[str] = "0-0"
    location: Optional[str] = None
    home: Optional[GameTeamResult] = GameTeamResult()
    away: Optional[GameTeamResult] = GameTeamResult()

    @property
    def home(self) -> GameTeamResult:
        return self.home

    @property
    def away(self) -> GameTeamResult:
        return self.away

    @property
    def date(self) -> str:
        date = datetime.fromisoformat(self._date)
        return date.strftime("%A \t %m/%d/%Y \t - \t %I:%M %p")
