from logging import Logger
from typing import List, Self

from client.client_url import ClientUrl
from client.playerdataservice.player_data_service_client import PlayerDataServiceClient
from mappers.player_response_mapper import PlayerDataServiceResponseMapper
from models.player import Player
from models.player_data_service_request import PlayerDataServiceRequest
from models.player_filters import PlayerFilters

logger = Logger("player_data_service_provider")


class PlayerDataServiceProvider:
    _client = PlayerDataServiceClient

    def __init__(self) -> Self:
        self._client = PlayerDataServiceClient()

    async def get_players_by_filters(self, filters: PlayerFilters) -> List[Player]:
        """
        Create request for the get by filters endpoint of the player data service response:
        """
        # TODO: Read limit from filter request
        url = ClientUrl("/player", "GET")
        request = PlayerDataServiceRequest()
        request.query_parameters = filters.to_dict()
        request.limit = 40
        request.order = "ASC"
        request.order_by = "number"
        response = await self._client.get_players_by_filters(request, url)

        players = list()
        if response is None or response.status != 200:
            players = []
        else:
            players = PlayerDataServiceResponseMapper.response_to_players(response.data)

        return players
