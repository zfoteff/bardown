from typing import Dict
from api.player_interface_router import PLAYER_INTERFACE_ROUTER
from client.cache.cache_client import CacheClient

class PlayerInterface:
    _config: Dict[str, str]

    def __init__(self, config: Dict[str, str]):
        self._config = config
        self.cache_config = CacheClient(config=config)
        self.routes = [PLAYER_INTERFACE_ROUTER]

    def shutdown(self) -> None:
        pass
