from bin.logger import Logger
from mq_client import RMQClient


class EventService:
    def __init__(self):
        self._client = RMQClient()

    def create_new_player_event(self, new_player_event: NewPlayerDocument) -> bool:
        pass
