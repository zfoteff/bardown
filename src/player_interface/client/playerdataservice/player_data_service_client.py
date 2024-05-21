from bin.logger import Logger
from models.player_data_service_request import PlayerDataServiceRequest
from models.player_data_service_response import PlayerDataServiceResponse
from requests import request
from requests.exceptions import ConnectionError, InvalidSchema

logger = Logger("player-data-service-client")


class PlayerDataServiceClient:
    async def get_players_by_filters(
        filters_request: PlayerDataServiceRequest,
    ) -> PlayerDataServiceResponse:
        """
        Call the get by filters endpoint of the PDS
        """
        try:
            res = request(
                method=filters_request.method,
                url=filters_request.url.url,
                params=filters_request.construct_query_parameters(),
                timeout=filters_request.url.connect_timeout_in_ms,
            )
            return PlayerDataServiceResponse(res.status_code, res.json()["data"])
        except InvalidSchema as e:
            logger.error(e)
            return PlayerDataServiceResponse(
                500,
                {
                    "message": "Schema error in request to Player Data Service",
                    "error": f"{e}",
                },
            )
        except ConnectionError as e:
            logger.error(f"Connection error reaching the Player Data Service: {e}")
            return PlayerDataServiceResponse(
                504,
                {
                    "message": "Connection error reaching the Player Data Service",
                    "error": f"{e}",
                },
            )
