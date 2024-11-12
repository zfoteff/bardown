from datetime import datetime

from models.enums.event_types import EventType
from pydantic import BaseModel


class Metadata(BaseModel):
    event_id: str
    event_type: EventType
    author: str
    event_created: datetime
