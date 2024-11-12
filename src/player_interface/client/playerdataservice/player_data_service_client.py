from models.player_data_service_request import PlayerDataServiceRequest
from models.player_data_service_response import PlayerDataServiceResponse
from requests import request
from requests.exceptions import ConnectionError, InvalidSchema

from bin.logger import Logger

logger = Logger("player-data-service-client")


class PlayerDataServiceClient:
    async def exchange_with_query_parameters(
        req: PlayerDataServiceRequest,
    ) -> PlayerDataServiceResponse:
        """
        Call the get by filters endpoint of the PDS
        """
        try:
            res = request(
                method=req.method,
                url=req.url.url,
                params=req.construct_query_parameters(),
                timeout=req.url.connect_timeout_in_ms,
            )

            if res.status_code != 200:
                return PlayerDataServiceResponse(res.status_code, {})

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
