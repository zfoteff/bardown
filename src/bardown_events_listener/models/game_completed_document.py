from models.document import Document


class GameCompletedDocument(Document):
    gameid: str
    score: str
    teams: List[Team]
