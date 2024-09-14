import datetime
from typing import Optional
from uuid import NAMESPACE_OID, uuid5

from bin.logger import Logger
from event_builder import EventBuilder
from event_service import EventService
from fastapi import Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.enums.event_types import EventType
from models.event import Event
from models.metadata import Metadata
from models.new_coach_document import NewCoachDocument
from models.new_player_document import NewPlayerDocument

logger = Logger("bardown-events-listener")
event_service = EventService()
event_builder = EventBuilder()


class EventsController:
    def _validate_user_token(self, user_token: Optional[str]) -> str:
        # TODO: Make it validate against list of approved authors
        return "UNKNOWN_AUTHOR" if user_token is None or user_token == "" else user_token

    async def create_new_player_event(
        self, new_player_event: NewPlayerDocument, user_token: Optional[str] = Header(None)
    ) -> JSONResponse:
        author = self._validate_user_token(user_token)

        try:
            metadata = Metadata(
                event_id=uuid5(
                    NAMESPACE_OID,
                    name=f"{new_player_event.first_name}+{new_player_event.last_name}+{author}",
                ),
                event_type=EventType.PLAYER_ADDED_TO_TEAM,
                author=author,
                event_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            event = Event(metadata=metadata, document=new_player_event)
            result = event_service.create_new_player_event(event)
        except Exception as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={"status": 403, "error": {"message": "Failed to publish message"}},
            )

        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(event)}
        )

    async def create_new_coach_event(self, new_coach_event: NewCoachDocument) -> JSONResponse:
        pass
