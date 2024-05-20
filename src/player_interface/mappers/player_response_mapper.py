from typing import Iterable

from models.player import Player


class PlayerDataServiceResponseMapper:
    def player_data_service_response_to_players(data: Iterable) -> Player:
        return [Player(**player) for player in data]
