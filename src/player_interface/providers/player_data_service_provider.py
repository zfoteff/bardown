from logging import Logger
from typing import List, Self

from client.client_url import ClientUrl
from client.playerdataservice.player_data_service_client import PlayerDataServiceClient
from mappers.player_response_mapper import PlayerDataServiceResponseMapper
from models.player import Player
from models.player_data_service_request import PlayerDataServiceRequest
from models.player_filters import PlayerFilters
from client.cache.cache_client import CacheClient

logger = Logger("player-data-service-provider")


class PlayerDataServiceProvider:
    _player_data_service_client: PlayerDataServiceClient
    _cache_client: CacheClient

    def __init__(self) -> Self:
        self._player_data_service_client = PlayerDataServiceClient
        self._cache_client = CacheClient()

    async def get_players_by_filters(self, filters: PlayerFilters) -> List[Player]:
        """
        Create request for the get by filters endpoint of the player data service response:
        """
        url = ClientUrl("player", "GET")
        request = PlayerDataServiceRequest(url=url, query_parameters=filters.to_dict())
        full_request_url = url.url + request.query_string()

        result, response = self._cache_client.retrieve_response(full_request_url)

        if not result:
            # If url dne in cache, make request to PDS
            response = await self._player_data_service_client.get_players_by_filters(
                request
            )

        players = list()
        if response is None or response.status != 200:
            players = []
        else:
            players = (
                PlayerDataServiceResponseMapper.player_data_service_response_to_players(
                    response.data
                )
            )
            if not result:
                # If a there was a cache miss then cache the url and response
                self._cache_client.cache_response(
                    url=full_request_url, response=response
                )

        return players
