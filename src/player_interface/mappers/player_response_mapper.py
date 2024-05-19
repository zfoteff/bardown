from typing import Iterable

from models.player import Player


class PlayerDataServiceResponseMapper:
    def response_to_players(data: Iterable) -> Player:
        return [Player(**player) for player in data]
