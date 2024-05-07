from typing import Self
from bin.logger import Logger
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from models.player_data_service_response import PlayerDataServiceResponse

logger = Logger("player-data-service-client")

class PlayerDataServiceClient:
    PLAYER_COACH_ENDPOINT_PATH = "player/"
    TEAM_ENDPOINT_PATH = "team/"

    base_path: str

    def __init__(self, config: PlayerDataServiceEndpointConfig) -> Self:
        self.base_path = self._compose_base_path(config)

    def get_players_by_filters(self) -> PlayerDataServiceResponse:
        pass

    def get(self) -> PlayerDataServiceResponse:
        pass

    def _compose_base_path(self, config: PlayerDataServiceEndpointConfig) -> str:
        return f"{config.base_path}/{config._app_pathname}/{config.api_version}/"