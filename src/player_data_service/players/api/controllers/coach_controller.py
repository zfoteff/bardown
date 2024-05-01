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
from src.player_data_service.players.mappers.coach_mapper import coach_DAO_to_coach_DTO
from src.player_data_service.players.models.dto.coach import Coach

logger = Logger("coach-controller")
db_interface = CoachesDatabaseInterface()


class CoachController:
    @classmethod
    async def create_coach(coach: Coach) -> JSONResponse:
        """Create a coach record in the database

        Args:\n
            coach (Coach): Coach data to persist to the database

        Returns:\n
            JSONResponse: Created coach record
        """
        try:
            result = db_interface.create_coach(coach)
        except CoachValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": f"{err}"}
            )
        except CoachAlreadyExists as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "coach_id": f"{err.existing_coach_id}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403, content={"status": 403, "error": "Database error"}
            )

        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(coach)}
        )

    @classmethod
    async def get_coaches(request: Request) -> JSONResponse:
        """Retrieve coaches data from database with multiple filters and pagination

        Args:\n
            request (Request): Request for coaches data, containing fields for filtering and
            ordering responses:
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

        Returns:\n
            JSONResponse: Coaches data
        """
        try:
            filters = validate_get_coaches_query_parameters(request.query_params)
            result, coaches = db_interface.get_coaches(filters)
        except CoachValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": f"{err}"}
            )

        if not result:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": "Database error"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": []
                if (coaches == []) or (coaches is None)
                else [json_encoder(coach_DAO_to_coach_DTO(coach)) for coach in coaches],
            },
        )

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
