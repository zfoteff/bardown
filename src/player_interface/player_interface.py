from contextlib import asynccontextmanager
from typing import List, Self

from api.player_interface_router import PLAYER_INTERFACE_ROUTER
from config.player_interface_config import PlayerInterfaceBaseConfig
from fastapi import APIRouter, FastAPI

from bin.metadata import servers, tags


class PlayerInterface:
    _application_config: PlayerInterfaceBaseConfig
    _app: FastAPI
    _routes: List[APIRouter]

    def __init__(
        self, application_config: PlayerInterfaceBaseConfig = PlayerInterfaceBaseConfig()
    ) -> Self:
        self._application_config = application_config
        self._routes = [PLAYER_INTERFACE_ROUTER]
        self._app = FastAPI(
            title=self._application_config.app_name,
            description="Player Interface for the Bardown application",
            lifespan=PlayerInterface.lifespan,
            version=self._application_config.version,
            debug=self._application_config.debug,
            license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
            openapi_tags=tags,
            servers=servers,
        )
        self.debug = application_config.debug
        self.log_level = application_config.log_level
        self.version = application_config.version

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
