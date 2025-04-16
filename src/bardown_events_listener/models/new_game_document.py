from datetime import datetime
from typing import List

from models.document import Document
from models.enums.grade import Grade
from models.enums.position import Position
from models.team import Team


class NewGameDocument(Document):
    title: str
    date: datetime
    location: str
    location: str
    teams: List[Team]
