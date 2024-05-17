from typing import Self, Dict

from requests import request
from requests.exceptions import InvalidSchema, ConnectionError

from bin.logger import Logger
from client.client_url import ClientUrl
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from models.player_data_service_request import PlayerDataServiceRequest
from models.player_data_service_response import PlayerDataServiceResponse

logger = Logger("player-data-service-client")


class PlayerDataServiceClient:
    PLAYER_COACH_ENDPOINT_PATH = "player/"
    TEAM_ENDPOINT_PATH = "team/"

    _config: PlayerDataServiceEndpointConfig
    _base_path: str

    def __init__(self) -> Self:
        self._config = PlayerDataServiceEndpointConfig()
        self._base_path = self._compose_base_path(self._config)

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

        try:
            res = request(
                method=url.method,
                url=self._base_path + self.PLAYER_COACH_ENDPOINT_PATH + self._compose_query_string(filters_request.__dict__()),
                params=filters_request.query_parameters,
                timeout=self._config.connect_timeout_ms,
            )
            response_body = res.json()
            logger.debug(res)
            return PlayerDataServiceResponse(res.status_code, {"data": response_body['data']})
        except InvalidSchema as e:
            logger.error(e)
            response = PlayerDataServiceResponse(500, {"message": f"{e}"})
            return response
        except ConnectionError as e:
            logger.error(e)
            response = PlayerDataServiceResponse(504, {"message": f"{e}"})


    def _compose_base_path(self, config: PlayerDataServiceEndpointConfig) -> str:
        """
        Create base path for all requests based on environment configuration
        """
        return f"{config.base_url}/{config._app_pathname}/{config.api_version}/"

    def _compose_query_string(self, filters: Dict) -> str:
        logger.debug(filters)
        return ""