from typing import Self, Tuple

from redis import Redis
from redis.exceptions import ConnectionError, DataError
from bin.logger import Logger
from config.cache_config import CacheConfig
from models.player_data_service_response import PlayerDataServiceResponse

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
        logger.info(f"Connected to cache instance")

    def cache_response(
        self, url: str, response: PlayerDataServiceResponse
    ) -> bool:
        try:
            self._client.set(name=url, value=response.data, ex=self._config.ttl)
            logger.info(f"Cached value for {url}: {response.data}")
            return True
        except ConnectionError as e:
            logger.error(f"Connection error to cache: {e}")
            return False
        except DataError as e:
            logger.error(f"Error caching value {response.data}\n{e}")
            return False

    def retrieve_response(
        self, url: str
    ) -> Tuple[bool, PlayerDataServiceResponse | None]:
        try:
            cached_response = self._client.get(url)

            if cached_response is None:
                logger.info(f"Cache miss: {url}")
                return (False, None)

            logger.info(f"Cache hit: {url}")
            return (True, PlayerDataServiceResponse(200, data=cached_response))
        except ConnectionError as e:
            logger.error(f"Connection error to cache: {e}")
            return (False, PlayerDataServiceResponse(500, data={"message": f"{e}"}))
