from typing import List, Optional

from models.document import Document
from models.enums.grade import Grade
from models.enums.position import Position


class NewCoachDocument(Document):
    first_name: str
    last_name: str
    role: str
    since: str
    email: str
    phone_number: str
    imgurl: Optional[str] = ""
    teams: Optional[List[str]] = []
