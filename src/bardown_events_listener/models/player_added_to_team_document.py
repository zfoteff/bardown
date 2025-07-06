from typing import List

from models.document import Document


class PlayerAddedToTeam(Document):
    player_ids: List[str]
    team_id: str
