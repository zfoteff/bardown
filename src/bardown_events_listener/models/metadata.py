from datetime import datetime

from pydantic import BaseModel


class Metadata(BaseModel):
    event_id: str
    event_type: EventType
    author: str
    event_created: datetime
