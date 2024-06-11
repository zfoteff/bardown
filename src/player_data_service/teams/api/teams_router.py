from fastapi import APIRouter
from teams.api.controllers.teams_controller import TeamController

API_VERSION = "v0"
PLAYER_ROUTER = APIRouter(prefix=f"/players/{API_VERSION}")

# TEAMS ROUTES
PLAYER_ROUTER.add_api_route(
    path="/team", endpoint=TeamController.create_team, methods=["POST"], tags=["teams"]
)
PLAYER_ROUTER.add_api_route(
    path="/team", endpoint=TeamController.get_teams, methods=["GET"], tags=["teams"]
)
PLAYER_ROUTER.add_api_route(
    path="/team", endpoint=TeamController.update_team, methods=["PATCH"], tags=["teams"]
)
PLAYER_ROUTER.add_api_route(
    path="/team",
    endpoint=TeamController.delete_team,
    methods=["DELETE"],
    tags=["teams"],
)
