from errors.games_errors import GameAlreadyExists, GameDoesNotExist, GameValidationError
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from games.api.validators.games_query_validator import (
    validate_get_games_query_parameters,
)
from games.games_db_interface import GamesDBInterface
from games.mappers.game_mapper import game_DAO_to_game_DTO
from games.models.dto.game import Game

from bin.logger import Logger

logger = Logger("player-data-service-controller")
db_interface = GamesDBInterface()


class GameController:
    async def create_game(game: Game) -> JSONResponse:
        try:
            result = db_interface.create_game(game)
        except GameAlreadyExists as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "game_id": f"{err.existing_game_id}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={"status": 403, "error": {"message": "Database error"}},
            )

        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(game)}
        )

    async def get_games(request: Request) -> JSONResponse:
        try:
            filters = validate_get_games_query_parameters(request.query_params)
            result, games = db_interface.get_games(filters)
        except GameValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(
                status_code=400,
                content={"status": 400, "error": {"message": "Database error"}},
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": []
                if (games == []) or (games is None)
                else [jsonable_encoder(game_DAO_to_game_DTO(game)) for game in games],
            },
        )

    async def update_game(game_id: str, game: Game) -> JSONResponse:
        try:
            success = db_interface.update_game(game, game_id)
        except GameDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not success:
            return JSONResponse(status_code=400, content={"status": 400, "error": "Database error"})

        return JSONResponse(
            status_code=200, content={"status": 200, "data": jsonable_encoder(game)}
        )

    async def delete_game(game_id: str) -> JSONResponse:
        try:
            result = db_interface.delete_game(game_id)
        except GameDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(status_code=422, content={"status": 422, "error": "Database error"})

        return JSONResponse(status_code=200, content={"status": 200, "data": {"game_id": game_id}})
