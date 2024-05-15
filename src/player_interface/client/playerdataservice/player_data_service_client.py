from typing import Self
from bin.logger import Logger
import httpx
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from models.player_data_service_response import PlayerDataServiceResponse
from models.player_data_service_request import PlayerDataServiceRequest
from client.client_url import ClientUrl
from requests import request

logger = Logger("player-data-service-client")


class PlayerDataServiceClient:
    PLAYER_COACH_ENDPOINT_PATH = "player/"
    TEAM_ENDPOINT_PATH = "team/"

    _config: PlayerDataServiceEndpointConfig
    _base_path: str

    def __init__(self) -> Self:
        self._config = PlayerDataServiceEndpointConfig()
        self._base_path = self._compose_base_path(self.config)

    async def get_players_by_filters(
        self, filters_request: PlayerDataServiceRequest, url: ClientUrl
    ) -> PlayerDataServiceResponse:
        """
        Call the get by filters endpoint of the PDS
        """
        limit = 10
        offset = 0
        order = "ASC"
        order_by = "number"

        req = request(
            method=url.method,
            url=self._base_path + self.PLAYER_COACH_ENDPOINT_PATH + url.path,
            params=filters_request.query_parameters,
            timeout=self.config.connect_timeout_ms,
        )
        res = req.json()

    async def _compose_base_path(self, config: PlayerDataServiceEndpointConfig) -> str:
        """
        Create base path for all requests based on environment configuration
        """
        return f"{config.base_path}/{config._app_pathname}/{config.api_version}/"
