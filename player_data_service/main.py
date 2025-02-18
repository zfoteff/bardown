from typing import Dict, Self

from config.db_config import DatabaseConfig
from src.api.default_router import DEFAULT_ROUTER
from src.games.api.games_router import GAMES_ROUTER
from src.players.api.player_router import PLAYER_ROUTER
from src.stats.api.statistics_router import STATISTICS_ROUTER
from src.teams.api.teams_router import TEAMS_ROUTER

class PlayerDataService:
    _config: Dict[str, str]

    def __init__(self, config: Dict[str, str]) -> Self:
        self._config = config
        self.db_config = DatabaseConfig(config=self._config)
        self.routes = [DEFAULT_ROUTER, GAMES_ROUTER, PLAYER_ROUTER, STATISTICS_ROUTER, TEAMS_ROUTER]

    def shutdown(self) -> None:
        pass