import json
from typing import Dict, Self, Tuple

from config.cache_config import CacheConfig
from models.player_data_service_response import PlayerDataServiceResponse
from redis import Redis
from redis.exceptions import ConnectionError, DataError

from bin.logger import Logger

logger = Logger("cache")


class CacheClient:
    _config: CacheConfig

    def __init__(self) -> Self:
        self._config = CacheConfig()
        self._client = Redis(
            host=self._config.host,
            port=self._config.port,
            health_check_interval=10,
            socket_connect_timeout=5,
            retry_on_timeout=False,
            socket_keepalive=True,
        )

    def cache_response(self, url: str, response: PlayerDataServiceResponse) -> bool:
        response_bytes = json.dumps(response.data).encode("utf-8")
        try:
            self._client.set(
                name=url,
                value=response_bytes,
                ex=self._config.ttl,
            )
            logger.info(f"Cached value for {url}")
            return True
        except ConnectionError as e:
            logger.error(f"Connection error to cache: {e}")
            return False
        except DataError as e:
            logger.error(f"Error caching value {response.data}\n{e}")
            return False

    def retrieve_response(self, key: str) -> Tuple[bool, PlayerDataServiceResponse | None]:
        try:
            cached_response = self._client.get(key)
            if cached_response is None:
                logger.info(f"Cache miss: {key}")
                return (False, None)

            logger.info(f"Cache hit for {key}")
            return (
                True,
                PlayerDataServiceResponse(200, data=json.loads(cached_response.decode("utf-8"))),
            )
        except ConnectionError as e:
            logger.error(f"Connection error to cache: {e}")
            return (False, PlayerDataServiceResponse(500, data={"message": f"{e}"}))

    def cache_health(self) -> Dict[str, str]:
        try:
            res = self._client.ping()
            if res:
                return {"status": "UP", "response": res}
            else:
                return {"status": "DOWN", "response": res}
        except ConnectionError as e:
            return {"status": "DOWN", "error": str(e)}
