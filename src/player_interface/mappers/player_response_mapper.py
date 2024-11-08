from typing import Iterable, List

from models.composite_statistics import CompositeStatistics
from models.game import Game
from models.player import Player
from models.team import Team


class PlayerDataServiceResponseMapper:
    def player_data_service_response_to_players(data: Iterable) -> List[Player]:
        return [Player(**player) for player in data]

    def player_data_sevice_response_to_teams(data: Iterable) -> List[Team]:
        return [Team(**team) for team in data]

    def player_data_service_response_to_games(data: Iterable) -> List[Game]:
        return [Game(**game) for game in data]

    def player_data_service_response_to_composite_statistics(data: Iterable) -> CompositeStatistics:
        result = CompositeStatistics(games=[], seasons=[])
        return result