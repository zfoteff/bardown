from pydantic import BaseModel


class CompositeTeam(BaseModel):
    team_id: str = None
    team_name: str = None
    img_url: str = None
    