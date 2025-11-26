from logging import Logger
from typing import Annotated, Dict, List, Self, Tuple

import requests
from client.cache.cache_client import CacheClient
from client.client_url import ClientUrl
from client.playerdataservice.player_data_service_client import PlayerDataServiceClient
from config import player_data_service_config
from config.player_data_service_config import PlayerDataServiceConfig
from fastapi import Depends
from mappers.player_response_mapper import (
    player_data_service_response_to_composite_statistics,
    player_data_service_response_to_games,
    player_data_service_response_to_players,
    player_data_sevice_response_to_teams,
)
from models.composite_statistics import CompositeStatistics
from models.game import Game
from models.game_filters import GameFilters
from models.player import Player
from models.player_data_service_request import PlayerDataServiceRequest
from models.players_filters import PlayersFilters
from models.team import Team
from models.team_filters import TeamFilters

logger = Logger("player-data-service-provider")


class PlayerDataServiceProvider:
    _host: str
    _player_data_service_config: PlayerDataServiceConfig
    _cache_client: CacheClient

    def __init__(
        self,
        player_data_service_config: PlayerDataServiceConfig = Annotated[
            player_data_service_config.get_player_data_service_config(),
            Depends(player_data_service_config.get_player_data_service_config()),
        ],
    ) -> Self:
        self._player_data_service_client = PlayerDataServiceClient()
        self._cache_client = CacheClient()
        self._player_data_service_config = player_data_service_config
        self._get_player_url: ClientUrl = ClientUrl(
            "GET",
            path="players/v0/player",
            config=player_data_service_config,
        )
        self._get_statistics_url: ClientUrl = ClientUrl(
            "GET", path="statistics/v0/statistics", config=player_data_service_config
        )
        self._get_team_url: ClientUrl = ClientUrl(
            "GET", path="team/v0/", config=self._player_data_service_config
        )
        self._get_game_url: ClientUrl = ClientUrl(
            "GET", path="game/v0/", config=self._player_data_service_config
        )
        self._health_url: ClientUrl = ClientUrl(
            "GET", path="health/", config=self._player_data_service_client
        )

    async def get_players_by_filters(self, filters: PlayersFilters) -> List[Player]:
        """
        Create request for the get by filters endpoint of the player interface:
        """
        get_player_request = PlayerDataServiceRequest(
            url=self._get_player_url, query_parameters=filters.to_dict()
        )

        cache_result, response = self._cache_client.retrieve_response(get_player_request.uri)

        if not cache_result:
            response = await self._player_data_service_client.exchange_with_query_parameters(
                get_player_request
            )

        players = list()
        if response is None or response.status != 200:
            players = []
        else:
            players = player_data_service_response_to_players(response.data)
            if not cache_result:
                self._cache_client.cache_response(url=get_player_request.uri, response=response)

        return players

    async def get_player_with_statistics_by_filters(
        self, player_id: str
    ) -> Tuple[Player, CompositeStatistics]:
        """
        Get player with associated statistics for games and seasons
        """
        player_request = PlayerDataServiceRequest(
            url=self._get_player_url, query_parameters={"filter.playerId": player_id}
        )
        statistics_request = PlayerDataServiceRequest(
            url=self._get_statistics_url, query_parameters={"filter.player.playerId": player_id}
        )
        player_cache_result, get_player_response = self._cache_client.retrieve_response(
            player_request.uri
        )
        statistics_cache_result, get_statistics_response = self._cache_client.retrieve_response(
            statistics_request.uri
        )

        if not player_cache_result:
            get_player_response = (
                await self._player_data_service_client.exchange_with_query_parameters(
                    player_request.uri
                )
            )

        if not statistics_cache_result:
            get_statistics_response = (
                await self._player_data_service_client.exchange_with_query_parameters(
                    statistics_request.uri
                )
            )

        player_data = None
        statistics_data = None
        if get_player_response is not None and get_player_response.status == 200:
            player_data = player_data_service_response_to_players(get_player_response.data)

        if get_statistics_response is not None and get_statistics_response.status == 200:
            statistics_data = player_data_service_response_to_composite_statistics(
                get_statistics_response.data, order_by_year=True
            )

        return (player_data, statistics_data)

    async def get_teams_by_filters(self, filters: TeamFilters) -> List[Team]:
        """
        Create request for the get by filters endpoint of the teams interface:
        """
        get_team_request = PlayerDataServiceRequest(
            url=self._get_team_url, query_parameters=filters.to_dict()
        )

        result, response = self._cache_client.retrieve_response(get_team_request.uri)

        if not result:
            # If URL dne in cache, make request to PDS
            response = await self._player_data_service_client.exchange_with_query_parameters(
                get_team_request
            )

        teams = list()
        if response is None or response.status != 200:
            # TODO: Create error response handler
            teams = []
        else:
            teams = player_data_sevice_response_to_teams(response.data)
            if not result:
                self._cache_client.cache_response(url=get_team_request.uri, response=response)

        return teams

    # async def get_team_with_players_and_coaches_by_filters(self, team_id: str) -> Tuple[Team, CompositeTeam]:

    async def get_games_by_filters(self, filters: GameFilters) -> List[Game]:
        get_games_request = PlayerDataServiceRequest(
            url=self._get_game_url, query_parameters=filters.to_dict()
        )
        result, response = self._cache_client.retrieve_response(get_games_request.uri)

        if not result:
            response = await self._player_data_service_client.exchange_with_query_parameters(
                get_games_request
            )

        games = list()
        if response is None or response.status != 200:
            games = []
        else:
            games = player_data_service_response_to_games(response.data)
            if not result:
                self._cache_client.cache_response(url=get_games_request.uri, response=response)
        return games

    async def get_health(self) -> Dict:
        response = requests.get(self._health_url.url)
        return response.json()

    async def get_cache_health(self) -> Dict:
        return self._cache_client.cache_health()
