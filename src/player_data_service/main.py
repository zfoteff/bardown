from typing import Dict, Self

from config.db_config import DatabaseConfig
from api.default_router import DEFAULT_ROUTER
from games.api.games_router import GAMES_ROUTER
from players.api.player_router import PLAYER_ROUTER
from stats.api.statistics_router import STATISTICS_ROUTER
from teams.api.teams_router import TEAMS_ROUTER
from dotenv import load_dotenv
import os
import yaml
import re

class PlayerDataService:
    _config: Dict[str, str]

    def __init__(self, config: Dict[str, str] = None) -> Self:
        self._config = self._load_profile_configurations() if config is None else config
        self.db_config = DatabaseConfig(config=self._config)
        self.routes = [DEFAULT_ROUTER, GAMES_ROUTER, PLAYER_ROUTER, STATISTICS_ROUTER, TEAMS_ROUTER]

    def _load_profile_configurations(self) -> Dict[str, str]:
        load_dotenv()

        profile = os.environ["PROFILE"].strip().lower()

        match profile:
            case "local":
                config_file = "./config/local.application.yaml"
            case "local-compose":
                config_file = "./config/local-compose.application.yaml"
            case "dev":
                config_file = "./config/dev.application.yaml"
            case "prod":
                config_file = "./config/prod.application.yaml"
            case _:
                config_file = "./config/local.application.yaml"

        with open(config_file) as f:
            config_content = f.read()

        pattern = re.compile(r"\${(\w+)}")
        updated_content = re.sub(pattern, lambda match : os.environ.get(match.group(1), match.group(0)), config_content)

        content = yaml.safe_load(updated_content) 
        print(content)
        return content


    def shutdown(self) -> None:
        pass