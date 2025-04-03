from contextlib import asynccontextmanager
from typing import Dict, List, Self

from api.default_router import DEFAULT_ROUTER
from config.player_data_service_config import PlayerDataServiceBaseConfig
from fastapi import APIRouter, FastAPI
from games.api.games_router import GAMES_ROUTER
from players.api.player_router import PLAYER_ROUTER
from stats.api.statistics_router import STATISTICS_ROUTER
from teams.api.teams_router import TEAMS_ROUTER

from bin.metadata import servers, tags


class PlayerDataServiceApplication():
    _application_config: PlayerDataServiceBaseConfig
    _routes: List[APIRouter]

    def __init__(
        self,
        application_config: PlayerDataServiceBaseConfig = PlayerDataServiceBaseConfig(),
    ) -> Self:
        self._application_config = application_config
        self.version = application_config.version
        self.debug = application_config.debug
        self.log_level = application_config.log_level
        self._routes = [
            DEFAULT_ROUTER,
            GAMES_ROUTER,
            PLAYER_ROUTER,
            STATISTICS_ROUTER,
            TEAMS_ROUTER,
        ]
        self.app  = FastAPI(
            title="Player Data Service",
            description="Interface for player data for the Bardown application",
            lifespan=self.lifespan,
            version=self._application_config.version,
            debug=self._application_config.debug,
            routes=self._routes,
            license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
            openapi_tags=tags,
            servers=servers,
        )

    @asynccontextmanager
    async def lifespan(self):
        # --- Startup events ---
        # Startup events
        self.startup()
        # Event Loop
        yield
        # Shutdown events
        self.shutdown()

    # Future work to load config from yaml file
    # def _load_profile_configurations(self) -> Dict[str, str]:
    #     load_dotenv()

    #     profile = os.environ["PROFILE"].strip().lower()

    #     if profile == "local":
    #         config_file = "./config/local.application.yaml"
    #     if profile == "local-compose":
    #         config_file = "./config/local-compose.application.yaml"
    #     if profile == "dev":
    #         config_file = "./config/dev.application.yaml"
    #     if profile == "prod":
    #         config_file = "./config/prod.application.yaml"
    #     else:
    #         config_file = "./config/local.application.yaml"

    #     with open(config_file) as f:
    #         config_content = f.read()

    #     pattern = re.compile(r"\${(\w+)}")
    #     updated_content = re.sub(
    #         pattern, lambda match: os.environ.get(match.group(1), match.group(0)), config_content
    #     )

    #     content = yaml.safe_load(updated_content)
    #     return content

    def shutdown(self) -> None:
        pass
