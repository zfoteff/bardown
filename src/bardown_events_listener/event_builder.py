from datetime import datetime
from uuid import uuid5

from models.enums.event_types import EventType
from models.event import Event
from models.metadata import Metadata


class EventBuilder:
    def __init__(self):
        pass

    def _build_event_metadata(
        event_name: str, event_author: str, event_type: EventType
    ) -> Metadata:
        return Metadata(
            event_id=uuid5(NAMESPACE_OID, name=f"{event_name}+{event_author}"),
            event_type=event_type,
            author=event_author,
            event_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def build(self, event_name: str) -> Event:
        return Event(metadata=self._build_event_metadata(event_name, event_author, event_type))
