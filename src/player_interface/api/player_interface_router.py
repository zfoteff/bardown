from player_interface.api.controllers.player_controller import PlayerController
from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

PLAYER_INTERFACE_ROUTER = APIRouter()


PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/",
    endpoint=PlayerController.render_homepage,
    description="Render application homepage",
    methods=["GET"],
    response_class=HTMLResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/players",
    endpoint=PlayerController.render_players_page,
    description="Render players page",
    methods=["GET"],
    response_class=HTMLResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/players/{player_id}",
    endpoint=PlayerController.render_player_page,
    description="Render player page with statistics",
    methods=["GET"],
    response_class=HTMLResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/teams",
    endpoint=PlayerController.render_teams_page,
    description="Render teams page",
    methods=["GET"],
    response_class=HTMLResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/games",
    endpoint=PlayerController.render_game_page,
    description="Render games page",
    methods=["GET"],
    response_class=HTMLResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/health",
    endpoint=PlayerController.get_health,
    description="Healthcheck endpoint for Player Interface",
    methods=["GET"],
    response_class=JSONResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/favicon.ico",
    endpoint=PlayerController.get_favicon,
    description="Retrieve favicon",
    methods=["GET"],
    response_class=FileResponse,
    include_in_schema=False,
)
