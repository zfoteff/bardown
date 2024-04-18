__version__ = "0.1.0"
__author__ = "Zac Foteff"

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.logger import Logger
from src.player_data_service.errors.coaches_errors import (
    CoachAlreadyExists,
    CoachDoesNotExist,
    CoachValidationError,
)
from src.player_data_service.players.coaches_db_interface import (
    CoachesDatabaseInterface,
)
from src.player_data_service.players.models.dto.coach import Coach

logger = Logger("coach-controller")
db_interface = CoachesDatabaseInterface()


class CoachController:
    @classmethod
    async def create_coach(coach: Coach) -> JSONResponse:
        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(coach)}
        )

    @classmethod
    async def get_coaches(request: Request) -> JSONResponse:
        return JSONResponse(status_code=200, content={"status": 200, "data": []})

    @classmethod
    async def update_coach(coach_id: str, coach: Coach) -> JSONResponse:
        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(coach)}
        )

    @classmethod
    async def delete_coach(coach_id: str) -> JSONResponse:
        return JSONResponse(
            status_code=200, content={"status": 200, "data": {"coach_id": coach_id}}
        )
