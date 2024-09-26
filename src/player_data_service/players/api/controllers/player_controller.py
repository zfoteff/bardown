from bin.logger import Logger
from errors.players_errors import (
    PlayerAlreadyExists,
    PlayerDoesNotExist,
    PlayerValidationError,
)
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from players.api.validators.players_query_validator import (
    validate_get_players_query_parameters,
)
from players.mappers.player_mapper import player_DAO_to_player_DTO
from players.models.dto.player import Player
from players.player_db_interface import PlayerDatabaseInterface

logger = Logger("player-data-service-controller")
db_interface = PlayerDatabaseInterface()


class PlayerController:
    async def create_player(player: Player) -> JSONResponse:
        """Create player record in the database

        Args:\n
            player (Player): Player data to persist in the database

        Returns:\n
            JSONResponse: Created player record
        """
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
            filters = validate_get_players_query_parameters(request.query_params)
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
                    jsonable_encoder(player_DAO_to_player_DTO(player))
                    for player in players
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
            success = db_interface.update_player(player, player_id)
        except PlayerDoesNotExist as err:
            return JSONResponse(
                status_code=404, content={"status": 404, "error": f"{err}"}
            )

        if not success:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": "Database error"}
            )

        return JSONResponse(
            status_code=200,
            content={"status": 200, "data": jsonable_encoder(player)},
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
            return JSONResponse(
                status_code=404, content={"status": 404, "error": f"{err}"}
            )

        if not result:
            return JSONResponse(
                status_code=422, content={"status": 422, "error": "Database error"}
            )

        return JSONResponse(
            status_code=200, content={"status": 200, "data": {"player_id": player_id}}
        )
