from pydantic import BaseModel
from datetime import datetime


class Metadata(BaseModel):
    event_id: str
    event_type: EventType
    author: str
    event_created: datetime
