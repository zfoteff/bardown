from typing import Self

from client.client_url import ClientUrl
from client.playerdataservice.player_data_service_client import PlayerDataServiceClient
from models.player_data_service_request import PlayerDataServiceRequest
from models.player_data_service_response import PlayerDataServiceResponse
from models.player_filters import PlayerFilters


class PlayerDataServiceProvider:
    _client = PlayerDataServiceClient

    def __init__(self) -> Self:
        self._client = PlayerDataServiceClient()

    def get_players_by_filters(
        self, filters: PlayerFilters
    ) -> PlayerDataServiceResponse:
        """
        Create request for the get by filters endpoint of the player data service response:
        """
        url = ClientUrl("/player", "GET")
        request = PlayerDataServiceRequest()
        response = self._client.get_players_by_filters(request, url)
        return response
