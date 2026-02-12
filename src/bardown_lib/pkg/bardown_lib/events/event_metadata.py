from uuid import uuid5, NAMESPACE_OID
from datetime import UTC, datetime
from pydantic import UUID5


class EventMetadata:
    event_id: UUID5 = uuid5(NAMESPACE_OID, datetime.now())
    triggered_by: str
    created: float = datetime.now(UTC).timestamp()
    modified: float = datetime.now(UTC).timestamp()