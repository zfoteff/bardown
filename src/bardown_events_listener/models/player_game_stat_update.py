from typing import List

from models.document import Document


class PlayerGameStatisticUpdate(Document):
    player_id: str
    statistics: str
