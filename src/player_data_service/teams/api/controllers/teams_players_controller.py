from errors.players_errors import PlayerDoesNotExist
from errors.teams_errors import TeamDoesNotExist, TeamValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from teams.models.dto.team_player import TeamPlayer
from teams.teams_db_interface import TeamsDBInterface
from validators.teams_query_validator import validate_team_player_request

from bin.logger import Logger

logger = Logger("team-controller")
teams_db_interface = TeamsDBInterface()


class TeamPlayersController:
    async def add_player_to_team_roster(team_player_request: TeamPlayer) -> JSONResponse:
        try:
            validated_team_player_request = validate_team_player_request(team_player_request)
            result = teams_db_interface.add_player_to_team(validated_team_player_request)
        except TeamValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
            )
        except PlayerDoesNotExist as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{validated_team_player_request.player_id}",
                    },
                },
            )
        except TeamDoesNotExist as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{validated_team_player_request.team_id}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                        "team_id": f"{validated_team_player_request.team_id}",
                    },
                },
            )

        return JSONResponse(
            status_code=201,
            content={"status": 201, "data": jsonable_encoder(validated_team_player_request)},
        )

    async def remove_player_from_team_roster(team_id: str, player_id: str) -> JSONResponse:
        pass
