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
from models.player_with_statistics import PlayerWithStatistics
from models.players_filters import PlayersFilters
from models.team import Team
from models.team_filters import TeamFilters

logger = Logger("player-data-service-provider")


class PlayerDataServiceProvider:
    _player_data_service_client: PlayerDataServiceClient
    _cache_client: CacheClient

    def __init__(self) -> Self:
        self._player_data_service_client = PlayerDataServiceClient
        self._cache_client = CacheClient()

    async def get_players_by_filters(self, filters: PlayersFilters) -> List[Player]:
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

    async def get_player_by_filters(self, player_id: str) -> PlayerWithStatistics:
        """Get player with associated statistics for games and seasons

        Args:
            player_id (str): _description_

        Returns:
            PlayerWithStatistics: _description_
        """
        get_player_url = ClientUrl("player", "GET", config=PlayerDataServiceEndpointConfig())
        get_statistics_url = ClientUrl(
            "statistics", "GET", config=PlayerDataServiceEndpointConfig()
        )
        player_request = PlayerDataServiceRequest(
            url=get_player_url, query_parameters={"player_id": player_id}
        )
        statistics_request = PlayerDataServiceRequest(
            url=get_player_url, query_parameters={"player_id": player_id}
        )
        full_get_player_request_url = get_player_url.url + player_request.query_string()
        full_get_statistics_request_url = get_statistics_url.url + statistics_request.query_string()

        result, get_player_response = self._cache_client.retrieve_response(
            full_get_player_request_url
        )
        result, get_statistics_response = self._cache_client.retrieve_response(
            full_get_statistics_request_url
        )

        if not result:
            get_player_response = (
                await self._player_data_service_client.exchange_with_query_parameters(
                    player_request
                )
            )
            get_statistics_response = (
                await self._player_data_service_client.exchange_with_query_parameters(
                    statistics_request
                )
            )

        player_data = None
        statistics_data = None
        if get_player_response is not None and get_player_response.status is 200:
            player_data = Player(**get_player_response.data)

        if get_statistics_response is not None and get_statistics_response is 200:
            statistics_data = PlayerDataServiceResponseMapper.player_data_service_response_to_composite_statistics(
                get_statistics_response.data
            )

        return PlayerWithStatistics(player_data, statistics_data)

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
