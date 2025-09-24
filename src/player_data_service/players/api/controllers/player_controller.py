from errors.players_errors import (
    PlayerAlreadyExists,
    PlayerDoesNotExist,
    PlayerRequestValidationError,
)
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from players.mappers.player_mapper import player_DAO_to_player_DTO
from players.models.dto.player import Player
from players.player_db_interface import PlayerDatabaseInterface
from validators.players_query_validator import validate_get_players_query_parameters

from bin.logger import Logger

logger = Logger("player-data-service-controller")
db_interface = PlayerDatabaseInterface()


class PlayerController:
    async def create_player(player: Player) -> JSONResponse:
        try:
            result = db_interface.create_player(player)
        except PlayerAlreadyExists as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "player_id": f"{err.existing_player_id}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={"status": 403, "error": {"message": "Database error"}},
            )

        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(player)}
        )

    async def get_players(request: Request) -> JSONResponse:
        try:
            filters = validate_get_players_query_parameters(request.query_params)
            result, players = db_interface.get_players(filters)
        except PlayerRequestValidationError as err:
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
                "data": (
                    []
                    if (players == []) or (players is None)
                    else [jsonable_encoder(player_DAO_to_player_DTO(player)) for player in players]
                ),
            },
        )

    async def update_player(player_id: str, player: Player) -> JSONResponse:
        try:
            success = db_interface.update_player(player, player_id)
        except PlayerDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not success:
            return JSONResponse(status_code=400, content={"status": 400, "error": "Database error"})

        return JSONResponse(
            status_code=200,
            content={"status": 200, "data": jsonable_encoder(player)},
        )

    async def delete_player(player_id: str) -> JSONResponse:
        try:
            result = db_interface.delete_players(player_id)
        except PlayerDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(status_code=422, content={"status": 422, "error": "Database error"})

        return Response(status_code=204)
