__version__ = "0.1.0"
__author__ = "Zac Foteff"
from api.controllers.default_controller import DefaultController
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

PLAYER_INTERFACE_ROUTER = APIRouter()


PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/",
    endpoint=DefaultController.render_homepage,
    description="Render application homepage",
    methods=["GET"],
    response_class=HTMLResponse,
)

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/statistics",
    endpoint=DefaultController.render_stats_page,
    description="Render statistics page",
    methods=["GET"],
    response_class=HTMLResponse,
)