from bin.logger import Logger
from fastapi import Request
from fastapi.responses import JSONResponse

from games.games_db_interface import GamesDBInterface

logger = Logger("player-data-service-controller")
db_interface = GamesDBInterface()


class GameController:
    def __init__(self) -> None:
        async def create_game(game: any) -> JSONResponse:
            pass

        async def get_games(request: Request) -> JSONResponse:
            pass

        async def update_game(game: any) -> JSONResponse:
            pass

        async  def delete_game(game: any) -> JSONResponse:
            pass