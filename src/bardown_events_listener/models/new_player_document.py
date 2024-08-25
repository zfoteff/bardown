from typing import Optional, List
from models.enums.grade import Grade
from models.enums.position import Position

from models.document import Document


class NewPlayerDocument(Document):
    first_name: str
    last_name: int
    number: int
    position: Position
    grade: Grade
    school: str
    imgurl: Optional[str] = ""
    teams: Optional[List[str]] = []
