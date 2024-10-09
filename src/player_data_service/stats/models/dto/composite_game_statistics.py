from pydantic import BaseModel


class CompositeGameStatistics(BaseModel):
    game_id: str = None
