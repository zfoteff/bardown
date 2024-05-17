__version__ = "0.1.0"
__author__ = "Zac Foteff"

from logging import Logger
from typing import Self

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from mappers.form_to_player_filters_mapper import PlayerFiltersMapper
from providers.player_data_service_provider import PlayerDataServiceProvider

templates = Jinja2Templates(directory="api/templates")
player_data_service_provider = PlayerDataServiceProvider()

logger = Logger("controller")

class DefaultController:
    def __init__(self) -> Self:
        self._player_data_service_provider = PlayerDataServiceProvider()

    async def render_homepage(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("home.html", context={"request": request})

    async def render_stats_page(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            "statistics.html", context={"request": request}
        )

    async def render_player_page(request: Request) -> HTMLResponse:
        logger.debug(str(request))
        filters = PlayerFiltersMapper.form_to_player_filters({})
        players = await player_data_service_provider.get_players_by_filters(filters)
        return templates.TemplateResponse(
            "players.html", context={"request": request, "players": players}
        )
