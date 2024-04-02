__version__ = "0.0.1"
__author__ = "Zac Foteff"

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.logger import Logger
from src.player_data_service.api.validators.players_query_validator import \
    validate_players
from src.player_data_service.errors.player_validation_error import \
    PlayerValidationError
from src.player_data_service.players.models.dto.player import Player
from src.player_data_service.players.player_db_interface import \
    PlayerDatabaseInterface

API_VERSION = "v0"

logger = Logger("player-data-service-controller")
db_interface = PlayerDatabaseInterface()


async def get_players(
    limit: int = None, offset: int = None, order: str = None, orderBy: str = None
) -> JSONResponse:

    try:
        valid_limit, valid_offset, valid_order = validate_players(
            limit, offset, order, orderBy
        )
        result, players = db_interface.get_players(limit, offset, valid_order)
    except PlayerValidationError as err:
        return JSONResponse(
            status_code=401, content={"status": 400, "error": {"message": f"{err}"}}
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
            "data": {}
            if (players == []) or (players is None)
            else {player.to_dict() for player in players},
        },
    )


async def create_player(player: Player) -> JSONResponse:
    result = db_interface.create_player(player)
    return JSONResponse(status_code=201, content={"status": 200, "data": f"{player}"})


PLAYER_DATA_SERVICE_CONTROLLER = APIRouter(prefix=f"/players/{API_VERSION}")
PLAYER_DATA_SERVICE_CONTROLLER.add_api_route(
    "/players", get_players, methods=["GET"], tags=["players"]
)
PLAYER_DATA_SERVICE_CONTROLLER.add_api_route(
    "/player", create_player, methods=["POST"], tags=["players"]
)
