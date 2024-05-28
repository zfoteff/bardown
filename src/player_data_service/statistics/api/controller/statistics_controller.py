__version__ = "0.1.0"
__author__ = "Zac Foteff"

from bin.logger import Logger
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from statistics.

logger = Logger("player-data-service-controller")

class StatisticsController:
    async def create_game_statistics(player_id) -> JSONResponse:
        pass
