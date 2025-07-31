from errors.teams_errors import TeamDoesNotExist, TeamValidationError
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from teams.api.validators.teams_query_validator import (
    validate_get_composite_team_query_parameters,
)
from teams.teams_db_interface import TeamsDBInterface

from bin.logger import Logger

logger = Logger("player-data-service-controller")
db_interface = TeamsDBInterface()


class CompositeTeamsController:
    async def get_composite_team(request: Request) -> JSONResponse:
        try:
            filters = validate_get_composite_team_query_parameters(request.query_params)
            result, teams = db_interface.get_composite_team(filters)
        except TeamDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})
        except TeamValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(
                status_code=422, content={"stauts": 422, "error": {"message": "Database error"}}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": jsonable_encoder(composite_teams_DAO_to_composite_teams_DTO(teams)),
            },
        )