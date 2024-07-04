from bin.logger import Logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from event_service import EventService
from models.new_player_document import NewPlayerDocument

logger = Logger("bardown-events-listener")
event_service = EventService()


class EventsController:
    async def create_new_player_event(self, new_player_event: NewPlayerDocument) -> JSONResponse:
        try:
            result = event_service.create_new_player_event(new_player_event)
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
            status_code=201, content={"status": 201, "data": jsonable_encoder(new_player_event)}
        )
