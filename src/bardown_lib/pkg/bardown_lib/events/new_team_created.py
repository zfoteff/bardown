from typing import Optional, List

from pkg.bardown_lib.events.event_metadata import EventMetadata

class TeamCreatedEvent:
    metadata: EventMetadata
    name: str
    location: str
    imgurl: str
    conference: str
    program_id: Optional[str] = None
    players: Optional[List[str]] = []
    coaches: Optional[List[str]] = []
