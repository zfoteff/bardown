from typing import List, Self

from player import Player
from player_data_service_response import PlayerDataServiceResponse


class PlayersResponse(PlayerDataServiceResponse):
    _players: List[Player]

    def __init__(self, status: int, players: List[Player]) -> Self:
        super().__init__(status=status, data=[player.to_dict() for player in players])
