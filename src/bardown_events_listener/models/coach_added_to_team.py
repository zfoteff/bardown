from typing import List

from models.document import Document


class CoachAddedToTeam(Document):
    coach_ids: List[str]
    team_id: str
