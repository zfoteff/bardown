__version__ = "0.1.0"
__author__ = "Zac Foteff"
from fastapi.responses import HTMLResponse
from api.controllers.default_controller import DefaultController
from fastapi import APIRouter

PLAYER_INTERFACE_ROUTER = APIRouter()

PLAYER_INTERFACE_ROUTER.add_api_route(
    path="/",
    endpoint=DefaultController.render_homepage,
    description="Render application homepage",
    methods=["GET"],
    response_class=HTMLResponse,
    tags=["home"],
)
