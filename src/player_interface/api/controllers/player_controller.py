import time

from fastapi import Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from main import __version__ as player_interface_version
from mappers.game_filters_mapper import GameFiltersMapper
from mappers.player_filters_mapper import PlayerFiltersMapper
from mappers.team_filters_mapper import TeamFiltersMapper
from providers.player_data_service_provider import PlayerDataServiceProvider

FAVICON_PATH = "static/favicon.ico"

start_time = time.time()
templates = Jinja2Templates(directory="api/templates")
player_data_service_provider = PlayerDataServiceProvider()


class PlayerController:
    async def get_favicon():
        return FileResponse(FAVICON_PATH)

    async def render_homepage(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("home.html", context={"request": request})

    async def render_game_page(request: Request) -> HTMLResponse:
        filters = GameFiltersMapper.form_to_game_filters({})
        games = await player_data_service_provider.get_games_by_filters(filters)
        return templates.TemplateResponse(
            "games.html", context={"request": request, "games": games}
        )

    async def render_season_stats_page(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("season_stats_page.html")

    async def render_teams_page(request: Request) -> HTMLResponse:
        filters = TeamFiltersMapper.form_to_team_filters({})
        teams = await player_data_service_provider.get_teams_by_filters(filters)
        return templates.TemplateResponse(
            "teams.html", context={"request": request, "teams": teams}
        )

    async def render_players_page(request: Request) -> HTMLResponse:
        filters = PlayerFiltersMapper.form_to_players_filters({})
        players = await player_data_service_provider.get_players_by_filters(filters)
        return templates.TemplateResponse(
            "players.html", context={"request": request, "players": players}
        )

    async def render_player_page(request: Request, player_id: str) -> HTMLResponse:
        player, statistics = await player_data_service_provider.get_player_by_filters(player_id)
        return templates.TemplateResponse(
            "player.html",
            context={"request": request, "data": {"player": player[0], "statistics": statistics}},
        )

    async def get_health() -> JSONResponse:
        """Healthcheck for the Player Interface service. Asserts the service is running and has
        connection to the Player Data Service

        Returns:
            JSONResponse: Healthcheck response
        """
        return JSONResponse(
            status_code=200,
            content={
                "status": "UP",
                "version": player_interface_version,
                "uptime": time.time() - start_time,
                "dependencies": {
                    "player_data_service": await player_data_service_provider.get_health(),
                    "cache": await player_data_service_provider.get_cache_health(),
                },
            },
        )
