from typing import List, Optional

from models.document import Document
from models.enums.grade import Grade
from models.enums.position import Position


class NewPlayerDocument(Document):
    first_name: str
    last_name: int
    number: int
    position: Position
    grade: Grade
    school: str
    imgurl: Optional[str] = ""
    teams: Optional[List[str]] = []
