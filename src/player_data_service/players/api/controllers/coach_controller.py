from errors.coaches_errors import (
    CoachAlreadyExists,
    CoachDoesNotExist,
    CoachValidationError,
)
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from players.api.validators.coaches_query_validator import (
    validate_get_coaches_query_parameters,
)
from players.coaches_db_interface import CoachesDatabaseInterface
from players.mappers.coach_mapper import coach_DAO_to_coach_DTO
from players.models.dto.coach import Coach

from bin.logger import Logger

logger = Logger("coach-controller")
db_interface = CoachesDatabaseInterface()


class CoachController:
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
            return JSONResponse(status_code=400, content={"status": 400, "error": f"{err}"})
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
            return JSONResponse(status_code=403, content={"status": 403, "error": "Database error"})

        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(coach)}
        )

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
                orderBy (str, optional): Field to order retrieved entries by. Acceptable
                values include:
                    - first_name
                    - last_name
                    - grade
                    - position

        Returns:\n
            JSONResponse: Coaches data
        """
        try:
            filters = validate_get_coaches_query_parameters(request.query_params)
            result, coaches = db_interface.get_coaches(filters)
        except CoachValidationError as err:
            return JSONResponse(status_code=400, content={"status": 400, "error": f"{err}"})
        except CoachDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(status_code=400, content={"status": 400, "error": "Database error"})

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": (
                    []
                    if (coaches == []) or (coaches is None)
                    else [jsonable_encoder(coach_DAO_to_coach_DTO(coach)) for coach in coaches]
                ),
            },
        )

    async def update_coach(coach_id: str, coach: Coach) -> JSONResponse:
        """Update a coach record in the database

        Args:\n
            coach_id (str): Coach id to retrieve and update
            coach (Coach): Coach values to update

        Returns:\n
            JSONResponse: Updated coach object
        """
        try:
            success = db_interface.update_coach(coach_id, coach)
        except CoachDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not success:
            return JSONResponse(status_code=400, content={"status": 400, "error": "Database error"})

        return JSONResponse(
            status_code=200, content={"status": 200, "data": jsonable_encoder(coach)}
        )

    async def delete_coach(coach_id: str) -> JSONResponse:
        """Delete a coach record from the database

        Args:\n
            coach_id (str): Coach ID of the coach record to delete from the database

        Returns:\n
            Response: Response with no content
        """
        try:
            result = db_interface.delete_coach(coach_id)
        except CoachDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(status_code=422, content={"status": 422, "error": "Database error"})

        return Response(status_code=204)
