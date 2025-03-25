import os
import re
from contextlib import asynccontextmanager
from typing import Dict, List, Self

import yaml
from api.default_router import DEFAULT_ROUTER
from config.db_config import DatabaseConfig
from config.player_data_service_config import PlayerDataServiceBaseConfig
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from games.api.games_router import GAMES_ROUTER
from players.api.player_router import PLAYER_ROUTER
from stats.api.statistics_router import STATISTICS_ROUTER
from teams.api.teams_router import TEAMS_ROUTER

from bin.metadata import servers, tags


class PlayerDataService:
    _application_config: Dict[str, str]
    _profile_config: Dict[str, str]
    _db_config: DatabaseConfig
    _routes: List[APIRouter]
    _version: str

    def __init__(
        self,
        application_config: PlayerDataServiceBaseConfig = None,
        profile_config: Dict[str, str] = None,
        version: str = "v0.0.0",
    ) -> Self:
        self._application_config = application_config
        self._profile_config = (
            self._load_profile_configurations() if profile_config is None else profile_config
        )
        self._version = version
        self._db_config = DatabaseConfig(config=self._profile_config)
        self._routes = [
            DEFAULT_ROUTER,
            GAMES_ROUTER,
            PLAYER_ROUTER,
            STATISTICS_ROUTER,
            TEAMS_ROUTER,
        ]

        self.app = FastAPI(
            title="Player Data Service",
            description="Interface for player data for the Bardown application",
            lifespan=self.lifespan,
            version=version,
            license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
            openapi_tags=tags,
            servers=servers,
        )

    @asynccontextmanager
    async def lifespan(self):
        # --- Startup events ---
        # Load routes
        for route in self.routes:
            self.app.include_router(route)
        # Event Loop
        yield

        # Shutdown events
        self.shutdown()

    def _load_profile_configurations(self) -> Dict[str, str]:
        load_dotenv()

        profile = os.environ["PROFILE"].strip().lower()

        if profile == "local":
            config_file = "./config/local.application.yaml"
        if profile == "local-compose":
            config_file = "./config/local-compose.application.yaml"
        if profile == "dev":
            config_file = "./config/dev.application.yaml"
        if profile == "prod":
            config_file = "./config/prod.application.yaml"
        else:
            config_file = "./config/local.application.yaml"

        with open(config_file) as f:
            config_content = f.read()

        pattern = re.compile(r"\${(\w+)}")
        updated_content = re.sub(
            pattern, lambda match: os.environ.get(match.group(1), match.group(0)), config_content
        )

        content = yaml.safe_load(updated_content)
        print(content)
        return content

    def shutdown(self) -> None:
        pass
