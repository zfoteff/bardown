from errors.teams_errors import TeamAlreadyExists, TeamDoesNotExist, TeamValidationError
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from teams.api.validators.teams_query_validator import (
    validate_get_teams_query_parameters,
)
from teams.mappers.team_mapper import team_DAO_to_team_DTO
from teams.models.dto.team import Team
from teams.teams_db_interface import TeamsDBInterface

from bin.logger import Logger

logger = Logger("team-controller")
db_interface = TeamsDBInterface()


class TeamController:
    async def create_team(team: Team) -> JSONResponse:
        """Create a team record in the database

        Args:
            team (Team): Team data to persist in the database

        Returns:
            JSONResponse: Created team record
        """
        try:
            result = db_interface.create_team(team)
        except TeamAlreadyExists as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{err.existing_team_id}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={"status": 403, "error": {"message": "Database error"}},
            )

        return JSONResponse(
            status_code=201, content={"status": 201, "data": jsonable_encoder(team)}
        )

    async def get_teams(request: Request) -> JSONResponse:
        """Retrieve team data from database with multiple filters and pagination

        Args:\n
            request (Request): Request for team data, containing fields for filtering and
            ordering the response:
                limit (int, optional): Limit the number of retrieved entries. Defaults to None.
                offset (int, optional): Offset to apply to retrieved entries. Defaults to None.
                order (str, optional): Ordering rules for retrieved values. Defaults to None.
                    - ASC
                    - DESC
                orderBy (str, optional): Field to order retrieved entries by. Acceptable
                values include:
                    - name

        Returns:\n
            JSONResponse: Team data
        """
        try:
            filters = validate_get_teams_query_parameters(request.query_params)
            result, teams = db_interface.get_team(filters)
        except TeamValidationError as err:
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
                if (teams == []) or (teams is None)
                else [jsonable_encoder(team_DAO_to_team_DTO(team)) for team in teams],
            },
        )

    async def update_team(team_id: str, team: Team) -> JSONResponse:
        """Update a team record in the database

        Args:\n
            team_id (str): Team id to retrieve and update
            team (Team): Team values to update

        Returns:\n
            JSONResponse: Updated team object
        """
        try:
            result = db_interface.update_team(team, team_id)
        except TeamDoesNotExist as err:
            return JSONResponse(status_code=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(status_code=400, content={"status": 400, "error": "Database error"})

        return JSONResponse(
            status_code=200, content={"status": 200, "data": jsonable_encoder(team)}
        )

    async def delete_team(team_id: str) -> JSONResponse:
        """Delete a team record from the database

        Args:\n
            team_id (str): Team ID of the team record to delete from the database

        Returns:\n
            Response: Response with no content
        """
        try:
            result = db_interface.delete_team(team_id)
        except TeamDoesNotExist as err:
            return JSONResponse(status=404, content={"status": 404, "error": f"{err}"})

        if not result:
            return JSONResponse(status_code=422, content={"status": 422, "error": "Database error"})

        return Response(status_code=204)
