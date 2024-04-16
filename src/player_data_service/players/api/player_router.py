__version__ = "0.1.0"
__author__ = "Zac Foteff"

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.logger import Logger
from src.player_data_service.errors.player_validation_error import (
    PlayerAlreadyExists,
    PlayerDoesNotExist,
    PlayerValidationError,
)
from src.player_data_service.players.api.validators.players_query_validator import (
    validate_get_players_query_parameters,
)
from src.player_data_service.players.mappers.player_mapper import (
    player_DAO_to_player_DTO,
)
from src.player_data_service.players.models.dto.player import Player
from src.player_data_service.players.player_db_interface import PlayerDatabaseInterface

API_VERSION = "v0"

logger = Logger("player-data-service-controller")
db_interface = PlayerDatabaseInterface()


async def create_player(player: Player) -> JSONResponse:
    """Create player record in the database

    Args:\n
        player (Player): Player data to persist in the database

    Returns:\n
        JSONResponse: Created player record
    """
    try:
        result = db_interface.create_player(player)
    except PlayerValidationError as err:
        return JSONResponse(
            status_code=401, content={"status": 400, "error": {"message": f"{err}"}}
        )
    except PlayerAlreadyExists as err:
        return JSONResponse(
            status=409,
            content={
                "status": 409,
                "error": {"message": f"{err}", "player_id": f"{err.player_id}"},
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
    """Retrieve player data from database with multiple filters and pagination

    Args:\n
        limit (int, optional): Limit the number of retrieved entries. Defaults to None.
        offset (int, optional): Offset to apply to retrieved entries. Defaults to None.
        order (str, optional): Ordering rules for retrieved values. Defaults to None.
            - ASC
            - DESC
        orderBy (str, optional): Field to order retrieved entries by. Acceptable values include:
            - number
            - first_name
            - last_name
            - position
        Defaults to None.

    Returns:\n
        JSONResponse: Player data
    """
    try:
        filters = validate_get_players_query_parameters(request)
        result, players = db_interface.get_players(filters)
    except PlayerValidationError as err:
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
            if (players == []) or (players is None)
            else [
                jsonable_encoder(player_DAO_to_player_DTO(player)) for player in players
            ],
        },
    )


async def update_player(player_id: str, player: Player) -> JSONResponse:
    """Update a player record in the database

    Args:\n
        player_id (str): Player_id to retrieve and update
        player (Player): Player values to update

    Returns:\n
        JSONResponse: Updated player object
    """
    try:
        success, result = db_interface.update_player(player_id, player)
    except PlayerDoesNotExist as err:
        return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

    return JSONResponse(
        status_code=200, content={"status": 200, "data": f"{player.model_dump_json()}"}
    )


async def delete_player(player_id: str) -> JSONResponse:
    """Delete a player record from the database

    Args:\n
        player_id (str): Player ID of the player record to delete from the database

    Returns:\n
        JSONResponse: Player ID of deleted record
    """
    try:
        result = db_interface.delete_players(player_id)
    except PlayerDoesNotExist as err:
        return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

    if not result:
        return JSONResponse(
            status_code=422, content={"status": 422, "error": f"Database error"}
        )

    return JSONResponse(
        status_code=200, content={"status": 204, "data": {"player_id": player_id}}
    )


PLAYER_ROUTER = APIRouter(prefix=f"/players/{API_VERSION}")
PLAYER_ROUTER.add_api_route(
    path="/players",
    endpoint=get_players,
    description="Retrieve player data from the database",
    methods=["GET"],
    tags=["players"],
    responses={
        200: {
            "description": "Players successfully found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": {
                                "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                "number": 6,
                                "first_name": "Zac",
                                "last_name": "Foteff",
                                "postion": "A",
                                "grade": "FR",
                                "school": "La Salle Catholic College Preparatory",
                            },
                        }
                    ],
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=create_player,
    description="Create player record in the database",
    methods=["POST"],
    tags=["players"],
    responses={
        201: {
            "description": "Players successfully created",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": {
                                "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                "number": 6,
                                "first_name": "Zac",
                                "last_name": "Foteff",
                                "postion": "A",
                                "grade": "FR",
                                "school": "La Salle Catholic College Preparatory",
                            },
                        }
                    ],
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=update_player,
    description="Update a player record in the database",
    methods=["PATCH"],
    tags=["players"],
    responses={
        200: {
            "description": "Players successfully updated",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": {
                                "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                "number": 6,
                                "first_name": "Zac",
                                "last_name": "Foteff",
                                "postion": "A",
                                "grade": "FR",
                                "school": "La Salle Catholic College Preparatory",
                            },
                        }
                    ],
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=delete_player,
    description="Delete a player record from the database",
    methods=["DELETE"],
    tags=["players"],
    responses={
        204: {
            "description": "Players successfully deleted from database",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 204,
                            "data": {
                                "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                            },
                        }
                    ],
                }
            },
        }
    },
)
