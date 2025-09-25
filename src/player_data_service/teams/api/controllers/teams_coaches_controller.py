from errors.coaches_errors import CoachDoesNotExist
from errors.teams_errors import TeamDoesNotExist, TeamValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from teams.models.dto.team_coach import TeamCoach
from teams.teams_db_interface import TeamsDBInterface
from validators.teams_query_validator import validate_team_coach_request

from bin.logger import Logger

logger = Logger("team-controller")
teams_db_interface = TeamsDBInterface()


class TeamCoachesController:
    async def add_coach_to_team_roster(team_coach_request: TeamCoach) -> JSONResponse:
        try:
            validated_team_coach_request = validate_team_coach_request(team_coach_request)
            result = teams_db_interface.add_coach_to_team(validate_team_coach_request)
        except TeamValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
            )
        except CoachDoesNotExist as err:
            return JSONResponse(
                status_code=404,
                content={
                    "status": 404,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{validated_team_coach_request.coach_id}",
                    },
                },
            )
        except TeamDoesNotExist as err:
            return JSONResponse(
                status_code=404,
                content={
                    "status": 404,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{validated_team_coach_request.team_id}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={
                    "status": 403,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{validated_team_coach_request.team_id}",
                    },
                },
            )

        return JSONResponse(
            status_code=201,
            content={"status": 201, "data": jsonable_encoder(validated_team_coach_request)},
        )
