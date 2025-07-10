__author__ = "Zac Foteff"
__version__ = "0.2.0"

from contextlib import asynccontextmanager
from typing import List, Self

from api.default_router import DEFAULT_ROUTER
from config.player_data_service_config import PlayerDataServiceBaseConfig
from fastapi import APIRouter, FastAPI
from games.api.games_router import GAMES_ROUTER
from players.api.player_router import PLAYER_ROUTER
from stats.api.statistics_router import STATISTICS_ROUTER
from teams.api.teams_router import TEAMS_ROUTER

from bin.metadata import servers, tags


class PlayerDataServiceApplication:
    _application_config: PlayerDataServiceBaseConfig
    _app: FastAPI
    _routes: List[APIRouter]

    def __init__(
        self,
        application_config: PlayerDataServiceBaseConfig = PlayerDataServiceBaseConfig(),
    ) -> Self:
        self._application_config = application_config
        self.version = __version__ 
        self.debug = application_config.debug
        self.log_level = application_config.log_level
        self._routes = [
            DEFAULT_ROUTER,
            GAMES_ROUTER,
            PLAYER_ROUTER,
            STATISTICS_ROUTER,
            TEAMS_ROUTER,
        ]
        self._app = FastAPI(
            title="Player Data Service",
            description="Interface for player data for the Bardown application",
            lifespan=PlayerDataServiceApplication.lifespan,
            version=self.version,
            debug=self._application_config.debug,
            license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
            openapi_tags=tags,
            servers=servers,
        )

        for route in self._routes:
            self._app.include_router(route)

    @property
    def app(self) -> FastAPI:
        return self._app

    @staticmethod
    @asynccontextmanager
    async def lifespan(app):
        # --- Startup events ---
        # Startup events
        app.state.startup_called = True
        # Event Loop
        yield
        # Shutdown events
        app.state.shutdown_called = True
