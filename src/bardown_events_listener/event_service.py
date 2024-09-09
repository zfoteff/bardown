from bin.logger import Logger
from models.event import Event
from mq_client import RMQClient


class EventService:
    def __init__(self):
        self._client = RMQClient()

    def create_new_player_event(self, new_player_event: Event) -> bool:
        pass

    def create_new_coach_event(self, new_coach_event: Event) -> bool:
        pass

    def create_new_game_event(self, new_game_event: Event) -> bool:
        pass

    def create_game_completed_event(self, game_completed_event: Event) -> bool:
        pass
