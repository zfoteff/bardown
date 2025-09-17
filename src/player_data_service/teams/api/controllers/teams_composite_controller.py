from errors.teams_errors import TeamDoesNotExist, TeamValidationError
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from validators.teams_query_validator import (
    validate_get_composite_team_query_parameters,
)
from teams.mappers.team_mapper import composite_team_DAO_to_composite_team_DTO
from teams.teams_db_interface import TeamsDBInterface

from bin.logger import Logger

logger = Logger("team-controller")
db_interface = TeamsDBInterface()


class CompositeTeamsController:
    async def get_composite_team(request: Request) -> JSONResponse:
        try:
            filters = validate_get_composite_team_query_parameters(request.query_params)
            result, composite_team = db_interface.get_composite_teams(filters)
        except TeamValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
            )
        except TeamDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": "Database error"}}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": jsonable_encoder(composite_team_DAO_to_composite_team_DTO(composite_team)),
            },
        )
