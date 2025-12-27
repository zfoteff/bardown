from pydantic import BaseModel


class GameResultTeam(BaseModel):
    score: int
    imgurl: str


class GameResult(BaseModel):
    game_id: str
    title: str
    home: GameResultTeam
    away: GameResultTeam
