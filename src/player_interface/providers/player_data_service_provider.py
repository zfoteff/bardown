from logging import Logger
from typing import List, Self

from client.cache.cache_client import CacheClient
from client.client_url import ClientUrl
from client.playerdataservice.player_data_service_client import PlayerDataServiceClient
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from mappers.player_response_mapper import PlayerDataServiceResponseMapper
from models.game import Game
from models.game_filters import GameFilters
from models.player import Player
from models.player_data_service_request import PlayerDataServiceRequest
from models.player_filters import PlayerFilters
from models.team import Team
from models.team_filters import TeamFilters

logger = Logger("player-data-service-provider")


class PlayerDataServiceProvider:
    _player_data_service_client: PlayerDataServiceClient
    _cache_client: CacheClient

    def __init__(self) -> Self:
        self._player_data_service_client = PlayerDataServiceClient
        self._cache_client = CacheClient()

    async def get_players_by_filters(self, filters: PlayerFilters) -> List[Player]:
        """
        Create request for the get by filters endpoint of the player interface:
        """
        url = ClientUrl("player", "GET", config=PlayerDataServiceEndpointConfig())
        request = PlayerDataServiceRequest(url=url, query_parameters=filters.to_dict())
        full_request_url = url.url + request.query_string()

        result, response = self._cache_client.retrieve_response(full_request_url)

        if not result:
            # If url dne in cache, make request to PDS
            response = await self._player_data_service_client.exchange_with_query_parameters(
                request
            )

        players = list()
        if response is None or response.status != 200:
            players = []
        else:
            players = PlayerDataServiceResponseMapper.player_data_service_response_to_players(
                response.data
            )
            if not result:
                # If a there was a cache miss then cache the url and response
                self._cache_client.cache_response(url=full_request_url, response=response)

        return players

    async def get_teams_by_filters(self, filters: TeamFilters) -> List[Team]:
        """
        Create request for the get by filters endpoint of the teams interface:
        """
        url = ClientUrl("team", "GET", config=PlayerDataServiceEndpointConfig())
        request = PlayerDataServiceRequest(url=url, query_parameters=filters.to_dict())
        full_request_url = url.url + request.query_string()

        result, response = self._cache_client.retrieve_response(full_request_url)

        if not result:
            # If URL dne in cache, make request to PDS
            response = await self._player_data_service_client.exchange_with_query_parameters(
                request
            )

        teams = list()
        if response is None or response.status != 200:
            # TODO: Create error response handler
            teams = []
        else:
            teams = PlayerDataServiceResponseMapper.player_data_sevice_response_to_teams(
                response.data
            )
            if not result:
                self._cache_client.cache_response(url=full_request_url, response=response)

        return teams

    async def get_games_by_filters(self, filters: GameFilters) -> List[Game]:
        url = ClientUrl("game", "GET", config=PlayerDataServiceEndpointConfig())
        request = PlayerDataServiceRequest(url=url, query_parameters=filters.to_dict())
        full_request_url = url.url + request.query_string()

        result, response = self._cache_client.retrieve_response(full_request_url)

        if not result:
            response = await self._player_data_service_client.exchange_with_query_parameters(
                request
            )

        games = list()
        if response is None or response.status != 200:
            games = []
        else:
            games = PlayerDataServiceResponseMapper.player_data_service_response_to_games(
                response.data
            )
            if not result:
                self._cache_client.cache_response(url=full_request_url, response=response)
        return games
