from typing import Self
from bin.logger import Logger
import httpx
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from models.player_data_service_response import PlayerDataServiceResponse
from client.client_url import ClientUrl
from requests import request

logger = Logger("player-data-service-client")


class PlayerDataServiceClient:
    PLAYER_COACH_ENDPOINT_PATH = "player/"
    TEAM_ENDPOINT_PATH = "team/"

    _config: PlayerDataServiceEndpointConfig
    base_path: str

    def __init__(self) -> Self:
        self._config = PlayerDataServiceEndpointConfig()
        self.base_path = self._compose_base_path(self.config)

    async def get_players_by_filters(self, url: ClientURL) -> PlayerDataServiceResponse:
        limit = 10
        offset = 0
        order = "ASC"
        order_by = "number"

        req = request(
            method=url.method,
            url=self.base_path + PLAYER_COACH_ENDPOINT_PATH + url.path,
            params=url.query_parameters,
            timeout=self.config.connect_timeout_ms,
        )
        res = req.json()

    async def _compose_base_path(self, config: PlayerDataServiceEndpointConfig) -> str:
        return f"{config.base_path}/{config._app_pathname}/{config.api_version}/"
