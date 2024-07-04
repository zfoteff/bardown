from bin.logger import Logger
from fastapi.responses import JSONResponse
from event_service import EventService
from models.new_player_document import NewPlayerDocument

logger = Logger("bardown-events-listener")
event_service = EventService()


class EventsController:
    async def create_new_player_event(self, new_player_event: NewPlayerDocument) -> JsonResponse:
        pass
