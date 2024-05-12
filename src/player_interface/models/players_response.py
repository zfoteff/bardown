from .player_data_service_response import PlayerDataServiceResponse
from typing import List, Self


class PlayersResponse(PlayerDataServiceResponse):
    _players: List

    def __init__(self, status: int) -> Self:
        super().__init__(status=status)
